# coding: utf-8

def lcs_match(sa, sb):
  matches = lcs(sa, sb)
  matches_num = len(matches)*1.
  f = 1.
  if len(sa) > 0 and len(sb) > 0:
    #f = matches_num/min(len(sa),len(sb))
    f = 2.*matches_num/(len(sa)+len(sb))
  return f

def lcs(a, b):
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = []
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result.append(a[x-1])
            x -= 1
            y -= 1
    return result
