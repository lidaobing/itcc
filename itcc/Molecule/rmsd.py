# $Id$

import sys
from itcc.Molecule import _rmsd
from itcc.Molecule import mtxyz

__revision__ = '$Rev$'
__all__ = ['rmsd']

debug = False

def rmsd(mol1, mol2):
    if debug:
        assert topeq(mol1, mol2)
    return _rmsd.rmsd(mol1, mol2)

def topeq(mol1, mol2):
    if len(mol1) != len(mol2):
        return False

    for i in range(len(mol1)):
        if mol1.atoms[i].no != mol2.atoms[i].no:
            return False
    return True

def usage(ofile):
    ofile.write('Usage:\n')
    ofile.write('    %s xyzfname1 mxyzfname2\n' % sys.argv[0])
    ofile.write('    %s mtxyzfname\n' % sys.argv[0])

def main():
    from itcc.Molecule import read
    if len(sys.argv) not in (2, 3):
        usage(sys.stderr)
        sys.exit(1)
    mol1 = read.readxyz(file(sys.argv[1]))
    for mol2 in mtxyz.Mtxyz(file(sys.argv[-1])):
        print rmsd(mol1, mol2)

if __name__ == '__main__':
    main()
