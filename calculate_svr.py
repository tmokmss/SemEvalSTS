# coding: utf-8
from svm import *
from svmutil import *
from data_classifier import *
import sts
import sys

def calculate_svr(data, label, c = 200, g = 0.02, p = 0.5, q = ''):
  prob = svm_problem(label, data)
  param = svm_parameter('-s 3 -t 2 -c %f -g %f -p %f %s' % (c, g, p, q))
  m = svm_train(prob, param)
  return m

def write_result(scores, fname):
  # libsvmのresultをsemeval形式に出力
  fout = open(fname, 'w')
  for score in scores:
    fout.write(str(score) + '\n')
  fout.close()

def grid_search(data, label, test_data, test_label):
  bestcorr = 0
  bestparams = None

  for c in (1,2,5,10,20,50,100,200,500,1000):
    for g in (1,.5,.2,.1,.05,.02,.01):
      for p in (2,1,.5,.2,.1,.05,.02,.01,.005,.002):
        model = calculate_svr(data, label, c, g, p, '-q')
        _, p_acc, _ = svm_predict(test_label, test_data, model, options='-q')
        corr = p_acc[2]
        if (corr > bestcorr):
          bestcorr = corr
          bestparams = (c, g, p)
          print "\n c=%f, g=%f, p=%f, corr=%f" % (c, g, p, corr)
        print '.',
  print 'bestcorr: ', bestcorr, 'bestparams:', bestparams
  return bestparams

def predict_scores(model, data, labels=None):
  if labels is None:
    labels = [0 for x in data]
  return svm_predict(labels, data, model, options='-q')

def load_model():
  model = {}
  for tclass in xrange(classNum):
    suffix = to_string(tclass)
    try:
      model[suffix] = svm_load_model(get_model_name(tclass))
    except:
      # 無ければ必ずあるshortのモデルを使う
      model[suffix] = svm_load_model(get_model_name(Short))
  return model

def predict_from_path(inputpath, outputpath):
  te_data, _ = sts.main(inputpath)
  model = load_model()
  tclasses = classify_from_path(inputpath)
  param = svm_parameter('-q')
  result = []
  for i in xrange(classNum):
    print to_string(i), tclasses.count(i)
  for datum, tclass in zip(te_data, tclasses):
    p_label, p_acc, p_val = predict_scores(model[to_string(tclass)], [datum])
    result.append(*p_label)
  write_result(result, outputpath)

def get_best_params(modelname):
  if to_string(VeryShort) in modelname:
    #return (200, 0.01, 1)
    return (1000, 0.1, 0.002)
  elif to_string(Short) in modelname:
    return (500, 0.05, 0.1)
  elif to_string(Unbalanced) in modelname:
    return (5, 1, 0.002)
  elif to_string(Long) in modelname:
    return (100, 1, 0.5)
  else:
    return (1,1,1)

if (__name__ == '__main__'):
  if len(sys.argv) < 6:
    print >>sys.stderr, "Usage: "
    print >>sys.stderr, "  %s train.txt train_scores.txt test.txt test_scores.txt output.txt" % sys.argv[0]
    exit(1)

  train_name = sys.argv[1]  # 教師データ
  train_score_name = sys.argv[2]  # 教師データのスコア
  test_name = sys.argv[3] # テストデータ
  test_score_name = sys.argv[4]  # テストデータのスコア
  out_name = sys.argv[5]  # モデル出力

  tr_data, tr_score = sts.main(train_name, train_score_name)

  best = get_best_params(out_name)
  if False :#or True:
    te_data, te_score = sts.main(test_name, test_score_name)
    best = grid_search(tr_data, tr_score, te_data, te_score)


  model = calculate_svr(tr_data, tr_score, *best)
  svm_save_model('model/' + out_name, model)
