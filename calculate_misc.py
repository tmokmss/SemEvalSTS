# coding: utf-8

def relative_len_difference(lca, lcb):
  # 文字列長による類似度
  la, lb = len(lca), len(lcb)
  return abs(la - lb) / float(max(la, lb) + 1e-5)
