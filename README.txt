The TakeLab Semantic Text Similarity System
===========================================

Version: 1.0
Release date: April 18, 2012


1 DESCRIPTION
=============

The TakeLab Semantic Text Similarity System was entered as task6-takelab-simple
in the SemEval-2012: Semantic Evaluation Exercises to perform the Semantic
Textual Similarity task: 

Given two sentences, s1 and s2, the system provides a similarity score as a
floating point number on the scale of 0 (no relation) to 5 (semantic
equivalence). The SemEval-2012 organizers measured the performance of our
system by comparing its output with the aggregated similarity scores obtained
from human subjects on the same data set using the Pearson correlation
coefficient. 

Please see http://www.cs.york.ac.uk/semeval-2012/task6/data/uploads/datasets/train-readme.txt
for more detailed information.


2 INSTRUCTIONS
==============

2.1 Installation prerequisites
------------------------------

This system requires the following packages: Python 2.7, NLTK, NumPy, and
LIBSVM.  If you are using Ubuntu Linux or a similar distribution, you can
install all of the prerequisites by typing:

        sudo apt-get install python-nltk python-numpy libsvm-tools


Once you install the NLTK package, you need to issue the following commands to
download the POS tagger model and the WordNet corpus:

        python -c "import nltk; nltk.download()"

When prompted, please select the maxent_treebank_pos_tagger model and the
wordnet corpus.


2.2 Download
------------

The source code and the data files can be downloaded from this location:

        http://takelab.fer.hr/sts/takelab_sts.tgz

If you use this software or its derivative to produce an academic publication,
please cite this work by using the citation listed on:

        http://takelab.fer.hr/sts



2.3 Usage
---------

Generating the features
-----------------------

Issuing

        python takelab_simple_features.py train/STS.input.MSRvid.txt train/STS.gs.MSRvid.txt > msrvid-train.txt
        python takelab_simple_features.py test/STS.input.MSRvid.txt > msrvid-test.txt

will generate the requisite features from the train/STS.input.MSRvid.txt and
test/STS.input.MSRvid.txt files respectively. Note: In order to avoid an
unreasonably large file download, the provided implementation contains the file
with the word frequencies (word-frequencies.txt) and the LSA word vectors
(nyt_words.txt, nyt_word_vectors.txt, wikipedia_words.txt and
wikipedia_word_vectors.txt) which were filtered to contain only the words
appearing in the official train and test sets. Using the larger unfiltered
datasets on the provided train and test sets will not affect the output of this
software in any way.


Obtaining the model parameters
------------------------------

Executing the provided shell script grid-search.sh

        ./grid-search.sh msrvid-train.txt

will find the optimal model parameters for the Support Vector Regression using
LIBSVM. The above command generates ends with the following output:

        Best correlation: 0.873686
        Type: svm-train -s 3 -t 2 -c 200 -g .02 -p .5 msrvid-train.txt model.txt

Thus the optimal LIBSVM parameters for msrvid-train.txt are:
-s 3 -t 2 -c 200 -g .02 -p .5.


Training
--------

By copy-pasting the command suggested by grid-search.sh, i.e. the text following "Type:"

        svm-train -s 3 -t 2 -c 200 -g .02 -p .5 msrvid-train.txt model.txt

one trains the model for MSR-Video corpus. 
The training will finish with the following output 
        .
        Warning: using -h 0 may be faster
        *.*
        optimization finished, #iter = 2777
        nu = 0.431544
        obj = -33239.258433, rho = -2.938525
        nSV = 337, nBSV = 311


Evaluation
----------

To evaluate the msrvid model against the msrvid test set, one can issue

        svm-predict msrvid-test.txt model.txt msrvid-output.txt

which should output the following:

        Mean squared error = 7.03655 (regression)
        Squared correlation coefficient = -nan (regression)

The obtained sentence similarity scores need postprocessing by the
postprocess_scores.py script

        python postprocess_scores.py test/STS.input.MSRvid.txt msrvid-output.txt

which handles some trivial corner cases of our scoring function. To obtain the
Pearson correlation, one can run the correlation.pl script which was provided
by the SemEval organizers alongside the training data:

        perl correlation.pl msrvid-output.txt test/STS.gs.MSRvid.txt

which outputs

        Pearson: 0.88516

indicating that the sentence similarity scores produced by our system have the
Pearson correlation of 0.88516 when compared to the similarity scores reported
by the human subjects (contained in the file test/STS.gs.MSRvid.txt). Please
note that the system that we provide on this page differs slightly from the
system that was submitted to SemEval. A couple of features described in the
paper are not used in this implementation (in particular sentence length and
the number of differing lemmas) and the implementation of some features might
be slightly different. Please email us if you notice any major differences.


2.4 Additional data
-------------------

We used the Google Books Ngrams dataset to obtain word frequencies. The
word-frequencies.txt file provided herein is filtered to only the words
appearing in the train and test sets. However, providing a larger, unfiltered
file does not change the output of the system in any way. Several features use
the word LSA vectors obtained from the Wikipedia and New York Times Annotated
Corpus. Since the full matrices containing all the LSA vectors are very large,
we provide only the shortened versions containing the vectors corresponding to
train and test set words. If you are interested in full matrices or the code
that generates them, please email frane.saric@fer.hr.



3. LICENSE
==========

This code is available under a derivative of a BSD-license that requires proper
attribution. Essentially, you can use, modify and sell this software or the
derived software in academic and non-academic, commercial and non-commercial,
open-source and closed-source settings, but you have to give proper credit.
