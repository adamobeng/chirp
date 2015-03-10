emojis = defaultdict(list)
for r in csv.reader(open('./emoji.tsv'), delimiter='\t'):
    emojis[r[1]].append(r[0])


def emoji_syn(word):
    if word in emojis:
        return emojis[word]
    else:
        return []

def unicode_len(word):
    word = cgi.unescape(word)
    return len(unicodedata.normalize('NFC', word))

def wn_syns(word, depth):
    lemmas = wn.lemmas(word)
    lemnames = list(i.synset().lemmas()[0].name() for i in lemmas)
    if depth == 0:
        return lemnames
    else:
        return [j for s in lemnames for j in wn_syns(s, depth-1)]

def shortest_syn(word, depth=0, emojionly=False):
    if emojionly: depth=max(depth, 3)
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

    if emojionly:
        options=list(es)

    print word, '=>', options, (depth, emojionly)
    if options:
        return ' '.join(options)
    else:
        return None


