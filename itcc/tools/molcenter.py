# $Id$
import sys
from numpy import array
from itcc.molecule import read

def molcenter(mol):
    total_coord = array((0.0, 0.0, 0.0))
    total_mass = 0.0
    for i in range(len(mol)):
        mass = mol.atoms[i].getmass()
        assert mass > 0, mol.atoms[i]
        total_mass += mass
        total_coord += mol.coords[i] * mass
    return total_coord / total_mass

def main():
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s molfname\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    mol = read.readxyz(file(sys.argv[1]))
    res = molcenter(mol)
    for i in range(3):
        print res[i],
    print

if __name__ == '__main__':
    main()
