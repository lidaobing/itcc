# $Id$

import math

__revision__ = '$Rev$'
__all__ = ['rmsd']

debug = False

def rmsd(mol1, mol2):
    if debug:
        assert topeq(mol1, mol2)
    coords1 = mol1.coords
    coords2 = mol2.coords
    assert len(coords1) == len(coords2)

    result = 0.0
    for i in range(len(coords1)):
        length = (coords1[i] - coords2[i]).length()
        result += length * length

    result = math.sqrt(result/len(coords1))
    return result

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
    assert len(sys.argv) == 3
    mol1 = read.readxyz(file(sys.argv[1]))
    mol2 = read.readxyz(file(sys.argv[2]))
    print rmsd(mol1, mol2)

if __name__ == '__main__':
    main()
