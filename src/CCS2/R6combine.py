# $Id$
# -*- coding: utf8 -*-
from sets import Set
from itcc.Tools.xpermutations import xuniqueCombinations

__all__ = ["R6combine"]


def _valid_R6_combine(combine):
    """检验改combine是否合法"""
    fixpointset = Set()
    for R6 in combine:
        fixpointset.update([R6[0], R6[1], R6[5], R6[6]])
        
    varypointsets = []
    for R6 in combine:
        varypointsets.append(Set(R6[2:5]))

    for varypointset in varypointsets:
        if fixpointset & varypointset:
            return False

    for i in range(len(varypointsets)):
        for j in range(i+1, len(varypointsets)):
            if varypointsets[i] & varypointsets[j]:
                return False
    return True

def _R6s_combine_gen_num(R6s, R6_number):
    return [Set(x) for x in xuniqueCombinations(R6s, R6_number)
            if _valid_R6_combine(x)]



def _new_combine(combine, result):
    for x in result:
        if combine.issubset(x):
            return False
    return True


def R6combine1(R6s):
    max_R6_number = len(R6s) // 5
    min_R6_number = (len(R6s) - 1) // 9 + 1
    
    result = _R6s_combine_gen_num(R6s, max_R6_number)

    for i in range(max_R6_number-1, min_R6_number-1, -1):
        result.extend(filter(lambda x:_new_combine(x, result), _R6s_combine_gen_num(R6s, i)))

    return tuple([tuple(x) for x in result])

def R6combine2(R6s):
    R6_number = len(R6s) // 5
    doubleR6s = R6s * 2
    combinenum = len(R6s) % 5 + 5
    return tuple([tuple(doubleR6s[i:i+R6_number*5:5]) for i in range(combinenum)])

def R6combine3(R6s):
    return tuple([(R6,) for R6 in R6s])

if __name__ == '__main__':
    atomnum = 19
    atoms = range(atomnum)
    atoms += atoms
    R6s = [tuple(atoms[i:i+7]) for i in range(atomnum)]
    R6combines = R6combine(R6s, int(atomnum/5), int((atomnum-1)/9)+1)
    import pprint
    print len(R6combines)
    pprint.pprint(R6combines)
    print
    pprint.pprint(R6combine2(R6s, atomnum//5))
    print
    pprint.pprint(R6combine3(R6s))
    


