from flask import Flask, request, render_template, url_for
from nltk.corpus import wordnet as wn
import nltk.data
import csv
from collections import defaultdict
import re
from nltk.corpus import stopwords
import unicodedata
import cgi

stopwords = stopwords.words('english')

app = Flask(__name__)

emojis = defaultdict(list)
for r in csv.reader(open('./emoji.tsv'), delimiter='\t'):
    emojis[r[1]].append(r[0])

@app.route('/')
def hello_world():
    return render_template('landing.html')

def emoji_syn(word):
    if word in emojis:
        return emojis[word]
    else:
        return []

def unicode_len(word):
    word = cgi.unescape(word)
    return len(unicodedata.normalize('NFC', word))

def wn_syns(word, depth):
    print 'word', depth
    synset = wn.synsets(word)
    synnames = list(i.name() for s in synset for i in s.lemmas() ) + [word]
    if depth == 1:
        return synnames
    else:
        return [j for s in synnames for j in wn_syns(s, depth-1)]

def shortest_syn(word, depth=1):
    synnames = wn_syns(word, depth)
    shorter = set(i for i in synnames if len(i)<len(word))
    shorter = sorted(shorter, key=len)
    shorter = shorter[:10]

    es = set(i for word in synnames for i in emoji_syn(word))  # TODO Add emoji syn of synonyms
    
    is_sw = word in stopwords

    options = []
    if shorter:
        options.extend(shorter)
    if es:
        options.extend(es)
    if is_sw:
        options.append('&#0;')

    print word, '=>', options
    if options:
        return ' '.join(options)
    else:
        return None

@app.route('/spellcheck.php', methods=['GET', 'POST'])
def spellcheck():
    text = request.form.get('text') or request.args.get('text')
    depth = request.args.get('depth') or 1

    wordsin = re.split('\W+', text) #TODO tokenize properly

    wordsout = [{'o': text.find(w), 'l':len(w), 's':3, 'options': shortest_syn(w, depth)} for w in wordsin if shortest_syn(w)]

    return render_template('results.xml', words = wordsout, charschecked=len(text))


if __name__ == '__main__':
    app.run(debug=True)
