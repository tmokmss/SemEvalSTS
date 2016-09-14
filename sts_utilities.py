# coding: utf-8
from nltk.corpus import wordnet
from collections import defaultdict
import math
import re

to_wordnet_tag = {
  'NN':wordnet.NOUN,
  'JJ':wordnet.ADJ,
  'VB':wordnet.VERB,
  'RB':wordnet.ADV
}

stopwords = set([
"i", "a", "about", "an", "are", "as", "at", "be", "by", "for", "from",
"how", "in", "is", "it", "of", "on", "or", "that", "the", "this", "to",
"was", "what", "when", "where", "who", "will", "with", "the", "'s", "did",
"have", "has", "had", "were", "'ll"
])
#stopwords = set([])

frequency_path = 'resources/word-frequencies_org.txt'

word_matcher = re.compile('[^0-9,.(=)\\[\]/_`]+$')
num_matcher = re.compile('\d+(\.\d+)?')
def is_word(w):
  # 数字や記号など、単語でないものはFalse
  return word_matcher.match(w) is not None

def get_locase_words(spos):
  # 単語と品詞タグのタプルの配列から、単語のみ抽出して小文字に変換された配列を返す
  return [x[0].lower() for x in spos
      if is_word(x[0])]

def get_non_words(spos):
  return [num_matcher.match(x[0]).group()
    for x in spos if num_matcher.match(x[0]) is not None]

def get_lemmatized_words(sa):
  # 名詞、形容詞、動詞、副詞については原型に戻す
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
    rez.append(wlem.decode('utf-8'))
  return rez

def get_original_form_words(sa):
  return sa

def load_wweight_table(path):
  # 各単語のIDFの辞書を読み込み
  lines = open(path).readlines()
  wweight = defaultdict(float)
  if not len(lines):
    return (wweight, 0.)
  totfreq = int(lines[0])
  for l in lines[1:]:
    w, freq = l.split()
    freq = float(freq)
    if freq < 5:
      continue
    wweight[w.decode('utf-8')] = math.log(totfreq / freq)
  return wweight

#wweight = load_wweight_table('resources/word-frequencies.txt')
wweight = load_wweight_table(frequency_path)
