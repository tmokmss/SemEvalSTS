# coding: utf-8
import math
from sts_utilities import *

def get_tfidf_cos(la, lb):
  a2sum = 0
  b2sum = 0
  absum = 0
  lenla = len(la)*1.
  lenlb = len(lb)*1.
  for worda in la:
    idf = wweight[worda]
    tfa = la.count(worda)/lenla
    a2sum += (tfa*idf)**2
    if worda in lb:
      tfb = lb.count(worda)/lenlb
      absum += tfa*idf * tfb*idf
  for wordb in lb:
    idf = wweight[wordb]
    tfb = lb.count(wordb)/lenlb
    b2sum += (tfb*idf)**2
  if a2sum == 0 or b2sum == 0:
    return 0
  cossim = absum/(math.sqrt(a2sum*b2sum))
  return cossim
