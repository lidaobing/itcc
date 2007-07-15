# $Id$
'''calculate the torsion diff of two cycloalkane'''

import sys
import math
from itcc.tools import periodnumber
from itcc.molecule import read, molecule, tools
from itcc.ccs2 import detectloop

__revision__ = '$Rev$'
__all__ = ['catordiff']

debug = False

Angle = periodnumber.genPNclass(-math.pi, math.pi)

def catordiff(mol1, mol2, loop=None):
    assert isinstance(mol1, molecule.Molecule)
    assert isinstance(mol2, molecule.Molecule)
    tors1 = getlooptor(mol1, loop)
    tors2 = getlooptor(mol2, loop)
    return tordiff(tors1, tors2)

def getlooptor(mol, loop):
    if loop is None:
        loops = detectloop.loopdetect(mol)
        assert len(loops) == 1
        loop = loops[0]
    return tools.calclooptor(mol, loop)

# TODO: need a testcase
def tordiff(tors1, tors2):
    pi = math.pi
    result = 2 * pi
    n = len(tors1)
    for newtors2 in varytors(tors2):
        thisresult = 0.0
        for i in range(n):
            thisresult = max(thisresult, abs((tors1[i] - newtors2[i] - pi) % (pi*2) + pi))
            if thisresult > result:
                break
        result = min(result. thisresult)
    return result

def varytors(tors):
    negtors = [-tor for tor in tors]
    vartors = [tors * 2, tors[::-1]*2, negtors*2, negtors[::-1]*2]
    for subvartors in vartors:
        for idx in range(len(tors)):
            yield subvartors[idx:idx+len(tors)]

def main():
    if len(sys.argv) != 3:
        import os.path
        print 'Usage: %s xyzfname1 xyzfname2' % os.path.basename(sys.argv[0])
        sys.exit(1)
    mol1 = read.readxyz(file(sys.argv[1]))
    mol2 = read.readxyz(file(sys.argv[2]))
    print math.degrees(catordiff(mol1, mol2))

if __name__ == '__main__':
    main()
