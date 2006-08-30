# $Id$
import sys
from itcc.molecule import read, atom

__revision__ = '$Rev$'

def cmpxyztop(mol1, mol2):
    if cmpatoms(mol1, mol2):
        if cmpconnect(mol1, mol2):
            return True
    return False

def cmpatoms(mol1, mol2):
    if len(mol1) != len(mol2):
        print 'Atom numbers is not equal: %i vs %i' % (len(mol1),
                len(mol2))
        return False
    result = True
    for idx in range(len(mol1)):
        atom1 = mol1.atoms[idx]
        atom2 = mol2.atoms[idx]
        if atom1.no != atom2.no:
            print 'the %i atom is different: %s vs %s' % (idx+1,
                atom.atomchr(atom1.no), atom.atomchr(atom2.no))
            result = False
        elif atom1.type != atom2.type:
            print 'the %i atom\'s type is different: %i vs %i' % (idx+1,
                atom1.type, atom2.type)
            result = False
    return result

def cmpconnect(mol1, mol2):
    connect1 = mol1.connect
    connect2 = mol2.connect

    result = True

    for j in range(len(connect1)):
        for i in range(j):
            if connect1[i, j] != connect2[i, j]:
                print 'the connect condition of atom %i and %i is' \
                    'diffrent: %s vs %s' % (i+1, j+1, bool(connect1[i,j]),
                    bool(connect2[i,j]))
                result = False
    return result

def main():
    if len(sys.argv) != 3:
        print >> sys.stderr, 'Usage: %s xyzfname1 xyzfname2' % sys.argv[0]
        sys.exit(1)
    mol1 = read.readxyz(file(sys.argv[1]))
    mol2 = read.readxyz(file(sys.argv[2]))
    if cmpxyztop(mol1, mol2):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
