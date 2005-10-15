# $Id$

__revision__ = '$Rev$'

from itcc.Tools import dmddat
from itcc.Molecule import read, write, molecule

def dmddat2mtxyz(dmddatfname, molfname):
    aDmddat = dmddat.Dmddat(file(dmddatfname))
    mol = read.readxyz(file(molfname))

    for frame in aDmddat:
        assert len(frame) == len(mol)
        for i in range(len(frame)):
            mol.coords[i] = molecule.CoordType(frame[i])
        write.writexyz(mol)

def main():
    import sys
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: %s dmddatfname molfname" % sys.argv[0]
        sys.exit(1)
    dmddat2mtxyz(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
