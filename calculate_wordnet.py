from nltk.corpus import wordnet as wn

def sim(word1, word2, lch_threshold=2.15, verbose=False):
    """Determine if two (already lemmatized) words are similar or not.

    Call with verbose=True to print the WordNet senses from each word
    that are considered similar.

    The documentation for the NLTK WordNet Interface is available here:
    http://nltk.googlecode.com/svn/trunk/doc/howto/wordnet.html
    """
    results = []
    for net1 in wn.synsets(word1):
        for net2 in wn.synsets(word2):
            try:
                lch = net1.lch_similarity(net2)
            except:
                continue
            # The value to compare the LCH to was found empirically.
            # (The value is very application dependent. Experiment!)
            if lch >= lch_threshold:
                results.append((net1, net2))
    if not results:
        return False
    if verbose:
        for net1, net2 in results:
            print net1
            print net1.definition
            print net2
            print net2.definition
            print 'path similarity:'
            print net1.path_similarity(net2)
            print 'lch similarity:'
            print net1.lch_similarity(net2)
            print 'wup similarity:'
            print net1.wup_similarity(net2)
            print '-' * 79
    return True

def syn(word, lch_threshold=2.26):
    for net1 in wn.synsets(word):
        for net2 in wn.all_synsets():
            try:
                lch = net1.lch_similarity(net2)
            except:
                continue
            # The value to compare the LCH to was found empirically.
            # (The value is very application dependent. Experiment!)
            if lch >= lch_threshold:
                yield (net1, net2, lch)
