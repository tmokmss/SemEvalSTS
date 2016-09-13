# coding: utf-8
import gensim.models.word2vec as w2v
import nltk
from nltk.corpus import wordnet
from sts_utilities import *

modelname = 'resources/gensim_glove.6B.50d.txt'
model = None

def load_model(modelpath):
  global model
  print "loading started"
  model = w2v.Word2Vec.load_word2vec_format(modelname, binary=False)
  print "loading finished"

def get_similar_words(word):
  if model == None:
    load_model(modelname)
  try:
    sim_words = model.most_similar(word)
    return sim_words
  except:
    return None

def get_augmented_words(words, threshold = 0.8):
  # 類義語を単語集合に追加
  words_new = []
  for word in words:
    words_new += [word]
    sim_words = get_similar_words(word)
    if sim_words == None:
      continue
    sim_words = [sw[0] for sw in sim_words if sw[1] > threshold]
    sim_words = remove_mistaken_words(word, sim_words)
    words_new += sim_words
  return words_new

def remove_mistaken_words(word, sim_words):
  # 品詞が異なる単語を除去
  # 原型に戻す
  tag = nltk.pos_tag([word])[0][1]
  swords_new = []
  for sword in sim_words:
    stag = nltk.pos_tag([sword])[0][1]
    wtag = to_wordnet_tag.get(stag[:2])
    if wtag is None:
      # 名詞形容詞動詞副詞でないなら除外
      continue
    if tag[:2] != stag[:2]:
      # 品詞が異なるなら除外
      continue
    try:
      wlem = wordnet.morphy(sword.decode('utf-8'), wtag) or sword
    except:
      # 文字コードのエラー出たらとりあえず除外
      continue
    if wlem == word:
      # 結局同じ単語になったら除外
      continue
    swords_new.append(wlem)
  return swords_new

if (__name__ == "__main__"):
  load_model(modelname)
  print model.most_similar('target')
