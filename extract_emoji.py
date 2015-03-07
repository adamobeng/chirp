from bs4 import BeautifulSoup
import codecs
import cgi


def escape(code):
    return '&#x' + code[2:].lower() + ';'

soup = BeautifulSoup(open('./full-emoji-list.html').read())
out = codecs.open('emoji.tsv', 'wb', encoding='utf8')
for r in soup.find_all('tr'):
    cells = r.find_all('td')
    if cells:
        print (escape(cells[1].get_text()), cells[12].get_text())
        out.write('%s\t%s\n' % (escape(cells[1].get_text()), cgi.escape(cells[12].get_text())))
