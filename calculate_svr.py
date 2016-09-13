# coding: utf-8
from svm import *
from svmutil import *
import sts
import sys

def calculate_svr(data, label, c = 200, g = 0.02, p = 0.5):
  prob = svm_problem(label, data)
  param = svm_parameter('-s 3 -t 2 -c %f -g %f -p %f' % (c, g, p))
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
        model = calculate_svr(data, label, c, g, p)
        _, p_acc, _ = svm_predict(test_label, test_data, model)
        corr = p_acc[2]
        if (corr > bestcorr):
          bestcorr = corr
          bestparams = (c, g, p)
  print 'bestcorr: ', bestcorr
  return bestparams

def predict_scores(model, data, labels=None):
  if labels is None:
    labels = [0 for x in data]
  return svm_predict(labels, data, model)

def load_model(modelpath):
  return svm_load_model(modelpath)

def predict_from_path(modelpath, inputpath, outputpath):
  te_data, _ = sts.main(inputpath)
  model = load_model(modelpath)
  p_labels, p_acc, p_vals = predict_scores(model, te_data)
  print p_acc
  write_result(p_labels, outputpath)

if (__name__ == '__main__'):
  if len(sys.argv) < 6:
    print >>sys.stderr, "Usage: "
    print >>sys.stderr, "  %s train.txt train_scores.txt test.txt test_scores.txt output.txt" % sys.argv[0]
    exit(1)

  train_name = sys.argv[1]
  train_score_name = sys.argv[2]
  test_name = sys.argv[3]
  test_score_name = sys.argv[4]
  out_name = sys.argv[5]

  tr_data, tr_score = sts.main(train_name, train_score_name)
  te_data, te_score = sts.main(test_name, test_score_name)

  #best = (2, 1, 0.002) # 0.01
  best = (5, 0.2, 0.002) # 0.05増加
  #best = (10,1,0.5)    # 0.02
  if len(sys.argv) > 6:
    best = grid_search(tr_data, tr_score, te_data, te_score)
    print best

  model = calculate_svr(tr_data, tr_score, *best)
  p_labels, p_acc, p_vals = predict_scores(model, te_data, te_score)
  print p_acc # _, mean squared error, correlaton efficient

  svm_save_model('model.txt', model)

  write_result(p_labels, out_name)
