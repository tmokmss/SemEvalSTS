# coding: utf-8
import numpy
from numpy.linalg import norm
from nltk.corpus import wordnet
from collections import Counter
from sts_utilities import *

# ほぼtakelabのコピペ
# word2vecの学習済みデータを利用して、類義語を考慮した類似度計算を行う

class Sim:
  # 単語ベクトル表現を保持するクラス
  def __init__(self, words, vectors):
    self.word_to_idx = {a: b for b, a in
              enumerate(w.strip() for w in open(words))}
    self.mat = numpy.loadtxt(vectors)

  def bow_vec(self, b):
    # BoW b内の単語ベクトルを全て加算した（もちろん正規化も行う）ベクトルを返す
    vec = numpy.zeros(self.mat.shape[1])
    for k, v in b.iteritems():
      idx = self.word_to_idx.get(k, -1)
      if idx >= 0:
        vec += self.mat[idx] / (norm(self.mat[idx]) + 1e-8) * v
    return vec

  def calc(self, b1, b2):
    # BoWベクトル間のcos類似度
    v1 = self.bow_vec(b1)
    v2 = self.bow_vec(b2)
    return abs(v1.dot(v2) / (norm(v1) + 1e-8) / (norm(v2) + 1e-8))

nyt_sim = Sim('resources/nyt_words.txt', 'resources/nyt_word_vectors.txt')
wiki_sim = Sim('resources/wikipedia_words.txt', 'resources/wikipedia_word_vectors.txt')

def dist_sim(sim, la, lb):
  wa = Counter(la)
  wb = Counter(lb)
  # 単語の複数回登場は無視する
  d1 = {x:1 for x in wa}
  d2 = {x:1 for x in wb}
  return sim.calc(d1, d2)

def weighted_dist_sim(sim, lca, lcb):
  # DFに基づいた重み付けをして、BoWベクトルのcos類似度を計算
  wa = Counter(lca)
  wb = Counter(lcb)
  wa = {x: wweight[x] * wa[x] for x in wa}
  wb = {x: wweight[x] * wb[x] for x in wb}
  return sim.calc(wa, wb)

def calc_wn_prec(lema, lemb):
  rez = 0.
  for a in lema:
    ms = 0.
    for b in lemb:
      ms = max(ms, wpathsim(a, b))
    rez += ms
  return rez / len(lema)

def wn_sim_match(lema, lemb):
  f1 = 1.
  p = 0.
  r = 0.
  if len(lema) > 0 and len(lemb) > 0:
    p = calc_wn_prec(lema, lemb)
    r = calc_wn_prec(lemb, lema)
    f1 = 2. * p * r / (p + r) if p + r > 0 else 0.
  return f1

wpathsimcache = {}
def wpathsim(a, b):
  if a > b:
    b, a = a, b
  p = (a, b)
  if p in wpathsimcache:
    return wpathsimcache[p]
  if a == b:
    wpathsimcache[p] = 1.
    return 1.
  sa = wordnet.synsets(a)
  sb = wordnet.synsets(b)
  mx = max([wa.path_similarity(wb)
        for wa in sa
        for wb in sb
        ] + [0.])
  wpathsimcache[p] = mx
  return mx
