# $Id$

__revision__ = '$Rev$'

from itcc.molecule import mtxyz, molecule
from itcc.core import tools

def rg(mol):
    center = molecule.CoordType()
    mass = 0.0
    for i in range(len(mol)):
        thismass = mol.atoms[i].mass
        mass += thismass
        center += mol.coords[i] * thismass
    center /= mass

    result = 0.0
    for i in range(len(mol)):
        result += tools.length(mol.coords[i] - center) ** 2 * mol.atoms[i].mass
    result /= mass
    return result

def mtxyzrg(ifname):
    ifile = file(ifname)
    for mol in mtxyz.Mtxyz(ifile):
        print rg(mol)

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        print 'Usage: %s ifname' % os.path.basename(sys.argv[0])
        sys.exit(1)

    mtxyzrg(sys.argv[1])

if __name__ == '__main__':
    main()
