# $Id$
'''calculate the torsion diff of two cycloalkane'''

import sys
import math
from itcc.Tools import periodnumber
from itcc.Molecule import read, molecule
from itcc.CCS2 import loopdetect

__revision__ = '$Rev$'
__all__ = ['catordiff']

debug = False

Angle = periodnumber.genPNclass(-math.pi, math.pi)

def catordiff(mol1, mol2):
    assert isinstance(mol1, molecule.Molecule)
    assert isinstance(mol2, molecule.Molecule)
    tors1 = getlooptor(mol1)
    tors2 = getlooptor(mol2)
    return tordiff(tors1, tors2)

def getlooptor(mol):
    loops = loopdetect.loopdetect(mol)
    assert len(loops) == 1
    loop = loops[0]
    doubleloop = loop * 2
    tors = [mol.calctor(*doubleloop[i:i+4]) for i in range(len(loop))]
    return tors

def tordiff(tors1, tors2):
    assert len(tors1) == len(tors2)
    results = []
    tors1 = [Angle(tor) for tor in tors1]
    tors2 = [Angle(tor) for tor in tors2]
    for newtors2 in varytors(tors2):
        diff = max([abs(ang1 - ang2) for ang1, ang2 in zip(tors1, newtors2)])
        results.append((diff, newtors2))
    results.sort()
    if debug:
        print 'Torsion of mol1: ', ['%6.1f' % math.degrees(float(tor)) for tor in tors1]
        print 'Torsion of mol2: ', ['%6.1f' % math.degrees(float(tor)) for tor in tors2]
        print 'Torsion of mol3: ', ['%6.1f' % math.degrees(float(tor)) for tor in results[0][1]]
        print ['%5.1f' % math.degrees(result[0]) for result in results]
    return results[0][0]

def varytors(tors):
    negtors = [-tor for tor in tors]
    vartors = [tors * 2, tors[::-1]*2, negtors*2, negtors[::-1]*2]
    for subvartors in vartors:
        for idx in range(len(tors)):
            yield subvartors[idx:idx+len(tors)]

def main():
    global debug
    debug = True
    assert len(sys.argv) == 3
    mol1 = read.readxyz(file(sys.argv[1]))
    mol2 = read.readxyz(file(sys.argv[2]))
    print math.degrees(catordiff(mol1, mol2))

if __name__ == '__main__':
    main()
