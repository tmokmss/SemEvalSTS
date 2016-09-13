# coding: utf-8
import sys
import nltk
import re
from collections import defaultdict
from nltk.corpus import wordnet
from sts_utilities import *

def load_data(path):
  sentences_pos = []
  r1 = re.compile(r'\<([^ ]+)\>')
  r2 = re.compile(r'\$US(\d)')
  for l in open(path):
    # 行ごとに前処理→形態素解析
    l = l.decode('utf-8')
    l = l.replace(u'’', "'")
    l = l.replace(u'``', '"')
    l = l.replace(u"''", '"')
    l = l.replace(u"—", '--')
    l = l.replace(u"–", '--')
    l = l.replace(u"´", "'")
    l = l.replace(u"-", " ")
    l = l.replace(u"/", " ")
    l = l.replace(u";", " ")
    #l = l.replace(u"é", "e")
    l = r1.sub(r'\1', l)
    l = r2.sub(r'$\1', l)
    s = l.strip().split('\t')
    sa, sb = tuple(nltk.word_tokenize(s)
              for s in l.strip().split('\t'))
    # nltk.word_tokenizeによりpunctuationは分離される(isn't→is n'tなど)
    sa, sb = ([x.encode('utf-8') for x in sa],
          [x.encode('utf-8') for x in sb])

    for s in (sa, sb):
      for i in xrange(len(s)):
        if s[i] == "n't":
          s[i] = "not"
        elif s[i] == "'m":
          s[i] = "am"
    sentences_pos.append((nltk.pos_tag(sa), nltk.pos_tag(sb)))
    # ('man', 'NN')のような、単語と品詞タグのタプルによる配列
  return sentences_pos

def get_lemmatized_words_new(sa):
  # 名詞、形容詞、動詞、副詞については原型に戻す
  rez = []
  for w, wpos in sa:
    w = w.lower()
    if not is_word(w):
      continue
    wtag = to_wordnet_tag.get(wpos[:2])
    if wtag is None:
      wlem = w
    else:
      # 複数形→単数形、過去形→現在形などの変換
      # utf-8に一旦変換しないと、wordnetの中でエラー吐く
      wlem = wordnet.morphy(w.decode('utf-8'), wtag) or w
    rez.append(wlem)
  return rez

wweight = defaultdict(int)
totalnum = 0
def count_words(sa, sb):
  lema = get_lemmatized_words_new(sa)
  lemb = get_lemmatized_words_new(sb)
  global wweight, totalnum
  for word in lema:
    wweight[word] += 1
    totalnum += 1
  for word in lemb:
    wweight[word] += 1
    totalnum += 1

def write_file(path):
  fout = open(path, 'w')
  fout.write(str(totalnum) + '\n')
  items = wweight.items()
  for word, freq in sorted(items, key=lambda item: item[1], reverse=True):
    fout.write(word + ' ' + str(freq) + '\n')
  fout.close()

if __name__ == '__main__':
  input_name = sys.argv[1]

  for sp in load_data(input_name):
    count_words(*sp)
  write_file("word_frequency.txt")
