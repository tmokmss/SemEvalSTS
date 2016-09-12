REM %1 is input file, %2 is score file
REM generate feature vectors
python sts.py train.txt train\%1 train\%2
python sts.py test.txt test\%1

REM calculate svr Model
svm-train -s 3 -t 2 -c 200 -g .02 -p .5 train.txt model.txt

REM calculate regression
svm-predict test.txt model.txt output.txt

REM post-process
python postprocess_scores.py test\%1 output.txt

REM calculate pearson correlation
perl correlation-noconfidence.pl output.txt test\%2

REM process 12STS.input.MSRpar.txt 12STS.gs.MSRpar.txt
REM process 12STS.input.MSRvid.txt 12STS.gs.MSRvid.txt
REM process 13STS.input.headlines.txt 13STS.gs.headlines.txt
