# coding: utf-8
from collections import Counter
from sts_utilities import *

def make_ngrams(l, n):
  # 単語の配列lをngramのタプルの配列に変換
  rez = [l[i:(-n + i + 1)] for i in xrange(n - 1)]
  rez.append(l[n - 1:])
  return zip(*rez)

def weighted_match(lca, lcb):
  wa = Counter(lca)
  wb = Counter(lcb)
  wsuma = sum(wweight[w] * wa[w] for w in wa)
  wsumb = sum(wweight[w] * wb[w] for w in wb)
  wsum = 0.

  for w in wa:
    wd = min(wa[w], wb[w])
    wsum += wweight[w] * wd
  p = 0.
  r = 0.
  if wsuma > 0 and wsum > 0:
    p = wsum / wsuma
  if wsumb > 0 and wsum > 0:
    r = wsum / wsumb
  f1 = 2 * p * r / (p + r) if p + r > 0 else 0.
  return f1

# 結局diceが一番！
def jaccard(lena, lenb, lenmatch):
  return 1.*lenmatch/(lena+lenb-lenmatch)

def dice(lena, lenb, lenmatch):
  return 2.*lenmatch/(lena+lenb)

def simpson(lena, lenb, lenmatch):
  return 1.*lenmatch/min(lena, lenb)

def ngram_match(sa, sb, n, coeff = dice):
  nga = make_ngrams(sa, n)
  ngb = make_ngrams(sb, n)
  matches = 0
  c1 = Counter(nga)
  for ng in ngb:
    if c1[ng] > 0:
      c1[ng] -= 1
      matches += 1
  f1 = 1.
  if len(nga) > 0 and len(ngb) > 0:
    f1 = coeff(len(nga), len(ngb), matches)
  return f1

def ngram_123_match(sa, sb, coeff = dice):
  f = []
  for i in xrange(1, 4):
    f.append(ngram_match(sa, sb, i, coeff))
  return f

def num_match(sa, sb):
  # 数字があってたら類似度かなり高いはず
  numa = get_non_words(sa)
  numb = get_non_words(sb)
  f1 = ngram_match(numa, numb, 1)
  return f1

def unique_words_match(sa, sb):
  # 固有名詞
  ca = [x[0] for x in sa[1:] if x[0][0].isupper()]
  cb = [x[0] for x in sb[1:] if x[0][0].isupper()]
  f1 = ngram_match(ca, cb, 1)
  return f1
