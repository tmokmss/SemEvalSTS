#!/bin/bash

if [[ $# -ne 1 ]] ; then
    echo "Usage: $0 train.txt"
    exit 1
fi

bestcorr=-2

if ! which svm-train > /dev/null ; then
    echo "Please install libsvm tools first (svm-train)"
    exit 1
fi

for param_c in 1 2 5 10 20 50 100 200 500 1000 ; do
    for param_p in 1 .5 .2 .1 .05 .02 .01; do
        for param_g in 2 1 .5 .2 .1 .05 .02 .01 .005 .002; do
            params="-s 3 -t 2 -c $param_c -g $param_g -p $param_p"
            echo "Trying params: $params"
            corr=$(svm-train $params -v 10 -q $1 | tail -n 1 |
                   awk '{print $NF}')
            if $(echo $corr $bestcorr | awk '$1<$2 {exit 1}') ; then
                bestcorr=$corr
                bestparams=$params
                echo Best correlation: $(echo $corr | awk '{print sqrt($1)}')
                echo Best params: $bestparams
            fi
        done
    done
done
echo Best correlation: $(echo $bestcorr | awk '{print sqrt($1)}')
echo Type: svm-train $bestparams $1 model.txt
