# $Id$
'''custom function of peptide
'''

from itcc.ccs2 import base

__revision__ = '$Rev$'
__all__ = ['Peptide']

class Peptide(base.Base):
    def __init__(self, mol):
        base.Base.__init__(self, mol)
        self.mol = mol

    def getr6s(self, loopatoms, is_chain = False):
        if is_chain:
            raise NotImplementedError
        
        types = gettypes(self.mol, loopatoms)
        if ispair(types[-1], types[0]):
            types = types[1:] + types[:1]
            loopatoms = loopatoms[1:] + loopatoms[:1]

        idx = 0
        newloopatoms = []
        while idx < len(loopatoms) - 1:
            type1 = types[idx]
            type2 = types[idx+1]
            if ispair(type1, type2):
                newloopatoms.append((loopatoms[idx], loopatoms[idx+1]))
                idx += 2
            else:
                newloopatoms.append((loopatoms[idx],))
                idx += 1
        if idx == len(loopatoms) - 1:
            newloopatoms.append((loopatoms[-1],))
        else:
            assert idx == len(loopatoms)

        doubleloop = newloopatoms * 2

        for i in range(len(newloopatoms)):
            yield tuple(doubleloop[i:i+7])

    def getcombinations(self, R6s):
        for R6 in R6s:
            yield (R6,)

def gettypes(mol, idxs):
    result = []
    for idx in idxs:
        result.append(mol.atoms[idx].atomchr()+str(degree(mol, idx)))
    return result

def degree(mol, idx):
    return sum(mol.connect[idx])

def ispair(type1, type2):
    return (type1, type2) in [('C3', 'N3'), ('N3', 'C3')]


