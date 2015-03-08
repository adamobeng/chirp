from flask import Flask, request, render_template, url_for
from nltk.corpus import wordnet as wn
import nltk.data
import csv
from collections import defaultdict
import re
from nltk.corpus import stopwords

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

def shortest_syn(word):
    synset = wn.synsets(word)
    synnames = list(s.name().split('.')[0] for s in synset) + [word]
    shortest = min(synnames, key=len)

    es = emoji_syn(word)  # TODO Add emoji syn of synonyms
    
    is_sw = word in stopwords


    options = []
    if (shortest != word) and len(shortest) < len(word):
        options.append(shortest)
    if es:
        options.extend(es)
    if is_sw:
        options.append('&#0;')

    print word, synnames, '=>', options
    if options:
        return ' '.join(options)
    else:
        return None

@app.route('/spellcheck.php', methods=['GET', 'POST'])
def spellcheck():
    text = request.form.get('text') or request.args.get('text')
    wordsin = re.split('\W+', text) #TODO tokenize properly

    wordsout = [{'o': text.find(w), 'l':len(w), 's':3, 'options': shortest_syn(w)} for w in wordsin if shortest_syn(w)]

    return render_template('results.xml', words = wordsout, charschecked=len(text))


if __name__ == '__main__':
    app.run(debug=True)
