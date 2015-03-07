from flask import Flask, request, render_template, url_for
from nltk.corpus import wordnet as wn
import nltk.data
import csv

app = Flask(__name__)

emojis = {r[1]:r[0] for r in csv.reader(open('./emoji.tsv'), delimiter='\t')}

@app.route('/')
def hello_world():
    return render_template('index.html')

def emoji_syn(word):
    if word in emojis:
        return [emojis[word]]
    else:
        return []

def shortest_syn(word):
    synset = wn.synsets(word)
    synnames = list(s.name().split('.')[0] for s in synset) + [word]
    shortest = min(synnames, key=len)

    es = emoji_syn(word)
    print word, synnames, '=>', shortest, es
    if (shortest != word) and len(shortest) < len(word):
        return '    '.join([shortest] + es)
    elif es:
        return es[0]
    else:
        return None

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text') or request.args.get('text')
    text =text.split(' ') #TODO tokenize properly

    s = ' '.join(shortest_syn(w) for w in text)
    return render_template('results.html', text=s)

@app.route('/spellcheck.php', methods=['GET', 'POST'])
def spellcheck():
    text = request.form.get('text') or request.args.get('text')
    wordsin = text.split(' ') #TODO tokenize properly

    wordsout = [{'o': text.find(w), 'l':len(w), 's':3, 'options': shortest_syn(w)} for w in wordsin if shortest_syn(w)]

    return render_template('results.xml', words = wordsout, charschecked=len(text))


if __name__ == '__main__':
    app.run(debug=True)
