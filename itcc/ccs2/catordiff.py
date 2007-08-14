# $Id$
'''calculate the torsion diff of two cycloalkane'''

import sys
import math

from itcc.tools import periodnumber
from itcc.molecule import read, molecule, tools
from itcc.ccs2 import detectloop, tordiff

__revision__ = '$Rev$'
__all__ = ['catordiff']

debug = False

Angle = periodnumber.genPNclass(-math.pi, math.pi)

def catordiff(mol1, mol2, loop=None):
    assert isinstance(mol1, molecule.Molecule)
    assert isinstance(mol2, molecule.Molecule)
    tors1 = getlooptor(mol1, loop)
    tors2 = getlooptor(mol2, loop)
    return tordiff.torsdiff(tors1, tors2, True, 0, 1)

def getlooptor(mol, loop):
    if loop is None:
        loops = detectloop.loopdetect(mol)
        assert len(loops) == 1
        loop = loops[0]
    return tools.calclooptor(mol, loop)

def main():
    if len(sys.argv) != 3:
        import os.path
        sys.stderr.write('Usage: %s xyzfname1 xyzfname2\n'
                         'result unit is degree\n'
                          % os.path.basename(sys.argv[0]))
        sys.exit(1)
    mol1 = read.readxyz(file(sys.argv[1]))
    mol2 = read.readxyz(file(sys.argv[2]))
    print math.degrees(catordiff(mol1, mol2))

if __name__ == '__main__':
    main()
