# $Id$

import math
from itcc.Tools import tools

__all__ = ['getshakeHdata', 'shakeH']

def getshakeHdata(mol):
    """getshakeHdata(mol) -> dict
    """
    result = {}
    for Cidx in [i for i in range(len(mol))
                 if mol.atoms[i].no == 6]:
        result[Cidx] = [[], []]
        for nai in [x[0] for x in enumerate(mol.connect[Cidx]) if x[1]]:
            if mol.atoms[nai].no == 1:
                result[Cidx][1].append(nai)
            else:
                result[Cidx][0].append(nai)
    return result


CHlen = 1.113
CHlenx = CHlen * math.sqrt(2.0/3.0)
CHleny = CHlen * math.sqrt(1.0/3.0)

def shakeH(coords, shakeHdata, Cidxs = None):
    if Cidxs is None:
        Cidxs = shakeHdata.keys()
    for Cidx in Cidxs:
        data = shakeHdata[Cidx]
        assert len(data[0]) == 2, str((data, Cidx))
        coords[data[1][0]], coords[data[1][1]] = \
                            tools.shakeH2(coords[Cidx], coords[data[0][0]],
                                          coords[data[0][1]])  
    return

if __name__ == '__main__':
    import sys
    import pprint
    from itcc.Molecule.read import readxyz
    mol = readxyz(file(sys.argv[1]))
    pprint.pprint(getshakeHdata(mol))
