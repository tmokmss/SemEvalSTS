from nltk.corpus import wordnet

def calc_wn_prec(lema, lemb):
  rez = 0.
  for a in lema:
    ms = 0.
    for b in lemb:
      ms = max(ms, wpathsim(a, b))
    rez += ms
  return rez / len(lema)

def wn_sim_match(lema, lemb):
  f1 = 1.
  p = 0.
  r = 0.
  if len(lema) > 0 and len(lemb) > 0:
    p = calc_wn_prec(lema, lemb)
    r = calc_wn_prec(lemb, lema)
    f1 = 2. * p * r / (p + r) if p + r > 0 else 0.
  return f1

wpathsimcache = {}
def wpathsim(a, b):
  if a > b:
    b, a = a, b
  p = (a, b)
  if p in wpathsimcache:
    return wpathsimcache[p]
  if a == b:
    wpathsimcache[p] = 1.
    return 1.
  sa = wordnet.synsets(a)
  sb = wordnet.synsets(b)
  mx = max([wa.path_similarity(wb)
        for wa in sa
        for wb in sb
        ] + [0.])
  wpathsimcache[p] = mx
  return mx
