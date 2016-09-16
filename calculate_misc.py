# coding: utf-8
from sts_utilities import *

def relative_len_difference(lca, lcb):
  # 文字列長による類似度
  la, lb = len(lca), len(lcb)
  return abs(la - lb) / float(max(la, lb) + 1e-5)

def relative_ic_difference(lca, lcb):
  #wa = sum(wweight[x] for x in lca)
  #wb = sum(wweight[x] for x in lcb)
  wa = sum(max(0., wweight[x] - minwweight) for x in lca)
  wb = sum(max(0., wweight[x] - minwweight) for x in lcb)
  return abs(wa - wb) / (max(wa, wb) + 1e-5)
