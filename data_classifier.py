# coding: utf-8

classNum = 5
Unbalanced = 4
VeryShort = 1
Short = 2
Long = 3
#VeryLong = 5
Default = 0

enable = True   # 分類を有効にするか？無効ならmodel_default.txtを利用する

veryShortThres = 20
shortThres = 40
unbalancedThres = 15

def classify_from_path(textpath):
  return [classify(*(text.split("\t"))) for text in open(textpath)]

def classify(text1, text2):
  #　問題の種類を分類する
  # すっごい恣意的^^：
  if not enable:
    return Default
  count1 = len(text1.split())
  count2 = len(text2.split())
  tclass = Long
  if count1 < veryShortThres and count2 < veryShortThres:
    tclass = VeryShort
  elif abs(count1-count2) > unbalancedThres:
    tclass = Unbalanced
  elif count1 < shortThres and count2 < shortThres:
    tclass = Short
  return tclass

def choose_optimal_model(text1, text2):
  # 問題に最適なSVRモデルを選択する
  textclass = classify(text1, text2)
  return get_model_name(textclass1)

def get_model_name(textclass):
  suffix = to_string(textclass)
  return "model/model_%s.txt" % (suffix)

def to_string(textclass):
  if textclass == VeryShort:
    return "veryshort"
  elif textclass == Short:
    return "short"
  elif textclass == Long:
    return "long"
  #elif textclass == VeryLong:
  #  return "verylong"
  elif textclass == Unbalanced:
    return "unbalanced"
  return "default"
