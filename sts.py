# coding: utf-8
# takelabのものを'参考'にした　http://takelab.fer.hr/sts/

from nltk.corpus import wordnet
import nltk
import sys
import re
from sts_utilities import *
import calculate_w2v as w2v
import calculate_tfidf as tfidf
from calculate_match import *
from calculate_misc import *

def fix_compounds(a, b):
  # もしaのある連続した2単語の連結と同じ単語がbにあれば、連結する
  # e.g. hoge hoge → hogehoge
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
    l = l.replace(u",", " ")
    #l = l.replace(u"é", "e")
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
    sa, sb = fix_compounds(sa, sb), fix_compounds(sb, sa)
    sentences_pos.append((nltk.pos_tag(sa), nltk.pos_tag(sb)))
    # ('man', 'NN')のような、単語と品詞タグのタプルによる配列
  return sentences_pos

def calc_features(sa, sb):
  # sa, sbは類似度を比較する文章
  # それぞれ単語と形態素のタプルの配列

  # 単語だけ抽出し、さらに小文字に変換
  olca = get_locase_words(sa)
  olcb = get_locase_words(sb)

  numa = get_non_words(sa)
  numb = get_non_words(sb)
  # print numa, numb

  # ストップワードを除去
  lca = [w for w in olca if w not in stopwords]
  lcb = [w for w in olcb if w not in stopwords]

  # 重要な品詞のみ抽出
  lema = get_lemmatized_words(sa)
  lemb = get_lemmatized_words(sb)

  #auga = w2v.get_augmented_words(lema)
  #augb = w2v.get_augmented_words(lemb)
  #print auga, augb

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
      #ngram_match(auga, augb, 1),  # 語順めちゃくちゃなので1gramのみ
      tfidf.get_tfidf_cos(lema, lemb),
      #tfidf.get_tfidf_cos(auga, augb),
      #wn_sim_match(lema, lemb),
      weighted_match(olca, olcb),
      weighted_match(lema, lemb),
      #dist_sim(nyt_sim, lema, lemb),
      #dist_sim(wiki_sim, lema, lemb),
      #weighted_dist_sim(nyt_sim, lema, lemb),
      #weighted_dist_sim(wiki_sim, lema, lemb),
      relative_len_difference(lca, lcb),
      #relative_ic_difference(olca, olcb),
      num_match(numa, numb),
    ]
  return f

def main(input_name, score_name=None):
  print "starting", input_name
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

  print "finished", input_name
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

  #if (out_name != None):
  #  fout = open(out_name, 'w')
  #  for y, datum in zip(scores, data):
  #    fvec =  ' '.join('%d:%f' % (i + 1, x) for i, x in
  #              enumerate(datum))
  #    fout.write(str(y) + ' ' + fvec + '\n')
  #  fout.close()
