#coding: utf-8
# takelabのものを'参考'にした　http://takelab.fer.hr/sts/

import math
from nltk.corpus import wordnet
import nltk
from collections import Counter, defaultdict
import sys
import re
import numpy
from numpy.linalg import norm

class Sim:
  def __init__(self, words, vectors):
    self.word_to_idx = {a: b for b, a in
                        enumerate(w.strip() for w in open(words))}
    self.mat = numpy.loadtxt(vectors)

  def bow_vec(self, b):
    vec = numpy.zeros(self.mat.shape[1])
    for k, v in b.iteritems():
      idx = self.word_to_idx.get(k, -1)
      if idx >= 0:
        vec += self.mat[idx] / (norm(self.mat[idx]) + 1e-8) * v
    return vec

  def calc(self, b1, b2):
    v1 = self.bow_vec(b1)
    v2 = self.bow_vec(b2)
    return abs(v1.dot(v2) / (norm(v1) + 1e-8) / (norm(v2) + 1e-8))

stopwords = set([
"i", "a", "about", "an", "are", "as", "at", "be", "by", "for", "from",
"how", "in", "is", "it", "of", "on", "or", "that", "the", "this", "to",
"was", "what", "when", "where", "who", "will", "with", "the", "'s", "did",
"have", "has", "had", "were", "'ll"
])

to_wordnet_tag = {
  'NN':wordnet.NOUN,
  'JJ':wordnet.ADJ,
  'VB':wordnet.VERB,
  'RB':wordnet.ADV
}

#nyt_sim = Sim('nyt_words.txt', 'nyt_word_vectors.txt')
#wiki_sim = Sim('wikipedia_words.txt', 'wikipedia_word_vectors.txt')

def fix_compounds(a, b):
  sb = set(x.lower() for x in b)

  a_fix = []
  la = len(a)
  i = 0
  while i < la:
    if i + 1 < la:
      comb = a[i] + a[i + 1]
      if comb.lower() in sb:
        a_fix.append(a[i] + a[i + 1])
        i += 2
        continue
    a_fix.append(a[i])
    i += 1
  return a_fix

def load_data(path):
  sentences_pos = []
  r1 = re.compile(r'\<([^ ]+)\>')
  r2 = re.compile(r'\$US(\d)')
  for l in open(path):
    l = l.decode('utf-8')
    l = l.replace(u'’', "'")
    l = l.replace(u'``', '"')
    l = l.replace(u"''", '"')
    l = l.replace(u"—", '--')
    l = l.replace(u"–", '--')
    l = l.replace(u"´", "'")
    l = l.replace(u"-", " ")
    l = l.replace(u"/", " ")
    #l = l.replace(u"é", "e")
    l = r1.sub(r'\1', l)
    l = r2.sub(r'$\1', l)
    s = l.strip().split('\t')
    sa, sb = tuple(nltk.word_tokenize(s)
              for s in l.strip().split('\t'))
    sa, sb = ([x.encode('utf-8') for x in sa],
          [x.encode('utf-8') for x in sb])

    for s in (sa, sb):
      for i in xrange(len(s)):
        if s[i] == "n't":
          s[i] = "not"
        elif s[i] == "'m":
          s[i] = "am"
    sa, sb = fix_compounds(sa, sb), fix_compounds(sb, sa)
    sentences_pos.append((nltk.pos_tag(sa), nltk.pos_tag(sb)))
    # ('man', 'NN')のような、単語と品詞タグのタプルによる配列
  return sentences_pos

word_matcher = re.compile('[^0-9,.(=)\[\]/_`]+$')
def is_word(w):
  # 数字や記号など、単語でないものはFalse
  return word_matcher.match(w) is not None

def get_locase_words(spos):
  # 単語と品詞タグのタプルの配列から、単語のみ抽出して小文字に変換された配列を返す
  return [x[0].lower() for x in spos
      if is_word(x[0])]

def get_lemmatized_words(sa):
  # 見出し語の抽出（名詞、形容詞、動詞、副詞）
  rez = []
  for w, wpos in sa:
    w = w.lower()
    if w in stopwords or not is_word(w):
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

def make_ngrams(l, n):
  # 単語の配列lをngramのタプルの配列に変換
  rez = [l[i:(-n + i + 1)] for i in xrange(n - 1)]
  rez.append(l[n - 1:])
  return zip(*rez)

def ngram_match(sa, sb, n):
  nga = make_ngrams(sa, n)
  ngb = make_ngrams(sb, n)
  matches = 0
  c1 = Counter(nga)
  for ng in ngb:
    if c1[ng] > 0:
      c1[ng] -= 1
      matches += 1
  p = 0.
  r = 0.
  f1 = 1.
  if len(nga) > 0 and len(ngb) > 0:
    p = matches / float(len(nga))
    r = matches / float(len(ngb))
    f1 = 2 * p * r / (p + r) if p + r > 0 else 0.
  return f1

def calc_features(sa, sb):
  # sa, sbは類似度を比較する文章
  # それぞれ単語と形態素のタプルの配列

  # 単語だけ抽出し、さらに小文字に変換
  olca = get_locase_words(sa)
  olcb = get_locase_words(sb)

  # ストップワードを除去
  lca = [w for w in olca if w not in stopwords]
  lcb = [w for w in olcb if w not in stopwords]

  # 重要な品詞のみ抽出
  lema = get_lemmatized_words(sa)
  lemb = get_lemmatized_words(sb)
  #print lema, lemb

  f = []
  #f += number_features(sa, sb)
  #f += case_matches(sa, sb)
  #f += stocks_matches(sa, sb)
  f += [
      ngram_match(lca, lcb, 1),
      ngram_match(lca, lcb, 2),
      ngram_match(lca, lcb, 3),
      ngram_match(lema, lemb, 1),
      ngram_match(lema, lemb, 2),
      ngram_match(lema, lemb, 3),
      #wn_sim_match(lema, lemb),
      #weighted_word_match(olca, olcb),
      #weighted_word_match(lema, lemb),
      #dist_sim(nyt_sim, lema, lemb),
      #dist_sim(wiki_sim, lema, lemb),
      #weighted_dist_sim(nyt_sim, lema, lemb),
      #weighted_dist_sim(wiki_sim, lema, lemb),
      #relative_len_difference(lca, lcb),
      #relative_ic_difference(olca, olcb)
    ]
  return f

def main(input_name, score_name=None):
  scores = None
  if score_name != None:
    scores = [float(x) for x in open(score_name)]

  data_v = []
  scores_v = []

  for idx, sp in enumerate(load_data(input_name)):
    y = 0. if scores is None else scores[idx]
    data = calc_features(*sp)
    data_v.append(data)
    scores_v.append(y)

  return data_v, scores_v

if __name__ == "__main__":
  if len(sys.argv) != 3 and len(sys.argv) != 4:
    print >>sys.stderr, "Usage: "
    print >>sys.stderr, "  %s output.txt input.txt [scores.txt]" % sys.argv[0]
    exit(1)

  score_name = None
  if len(sys.argv) >= 4:
    score_name = sys.argv[3]

  input_name = sys.argv[2]
  out_name = sys.argv[1]

  data, scores = main(input_name, score_name)

  if (out_name != no):
    fout = open(out_name, 'w')
    for y, datum in zip(scores, data):
      fvec =  ' '.join('%d:%f' % (i + 1, x) for i, x in
                enumerate(datum))
      fout.write(str(y) + ' ' + fvec + '\n')
    fout.close()
