from flask import Flask, request, render_template, url_for
from nltk.corpus import wordnet as wn
import nltk.data
import csv
from collections import defaultdict
import re
from nltk.corpus import stopwords
import unicodedata
import cgi
from util import *

stopwords = stopwords.words('english')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/spellcheck.php', methods=['GET', 'POST'])
def spellcheck():
    text = request.form.get('text') or request.args.get('text')
    depth = int(request.args.get('depth')) or 0
    emojionly = (request.args.get('emojionly') == 'true') or False

    wordsin = re.split('\W+', text) #TODO tokenize properly

    wordsout = [{'o': text.find(w), 'l':len(w), 's':3, 'options': shortest_syn(w, depth, emojionly)} for w in wordsin if shortest_syn(w)]

    return render_template('results.xml', words = wordsout, charschecked=len(text))


if __name__ == '__main__':
    app.run(debug=True)
