# $Id$

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

def main():
    import sys
    from itcc.Molecule import read
    if len(sys.argv) != 3:
        print 'Usage: %s xyzfname1 mxyzfname2' % sys.argv[0]
        sys.exit(1)
    mol1 = read.readxyz(file(sys.argv[1]))
    for mol2 in mtxyz.Mtxyz(file(sys.argv[2])):
        print rmsd(mol1, mol2)

if __name__ == '__main__':
    main()
