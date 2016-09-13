# coding: utf-8
import calculate_svr as svr
import sys

if (__name__ == '__main__'):
  if len(sys.argv) < 2:
    print >>sys.stderr, "Usage: "
    print >>sys.stderr, "  %s test.txt output.txt" % sys.argv[0]
    exit(1)

  datafile = sys.argv[1]    # 判定するテキスト
  outputfile = sys.argv[2]  # 結果（類似度）の出力先

  svr.predict_from_path(datafile, outputfile)
