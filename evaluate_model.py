# coding: utf-8
import calculate_svr as svr
import sys

if (__name__ == '__main__'):
  if len(sys.argv) < 3:
    print >>sys.stderr, "Usage: "
    print >>sys.stderr, "  %s model.txt test.txt output.txt" % sys.argv[0]
    exit(1)

  modelfile = sys.argv[1]
  datafile = sys.argv[2]
  outputfile = sys.argv[3]

  svr.predict_from_path(modelfile, datafile, outputfile)
