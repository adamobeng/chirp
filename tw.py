from flask import Flask, request, render_template
from nltk.corpus import wordnet as wn
import nltk.data

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

def shortest_syn(word):
    synset = wn.synsets(word)
    synnames = list(s.name().split('.')[0] for s in synset) + [word]
    shortest = min(synnames, key=len)
    print word, synnames, '=>', shortest
    return shortest

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text'].split(' ') #TODO tokenize properly

    s = ' '.join(shortest_syn(w) for w in text)

    return render_template('results.html', text=s)


if __name__ == '__main__':
    app.run(debug=True)
