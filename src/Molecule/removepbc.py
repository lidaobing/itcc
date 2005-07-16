# $Id$

__revision__ = '$Rev$'

from itcc.Molecule import read, write, molecule

def nearestmirror(coord, origin, pbc):
    result = [None] * 3
    for i in range(3):
        result[i] = (coord[i] - origin[i]) % pbc[i]
        if result[i] > pbc[i] / 2.0:
            result[i] -= pbc[i]
        result[i] += origin[i]
    return molecule.CoordType(result)

def removepbc(xyzfname, pbc):
    mol = read.readxyz(file(xyzfname))
    coords = mol.coords
    origin = coords[0]
    for i in range(1, len(coords)):
        coords[i] = nearestmirror(coords[i], origin, pbc)
    write.writexyz(mol)

def main():
    import sys
    if len(sys.argv) != 5:
        print >> sys.stderr, 'Usage: %s xyzfname pbc.x pbc.y pbc.z' % sys.argv[0]
        sys.exit(1)
    removepbc(sys.argv[1], [float(x) for x in sys.argv[2:5]])

if __name__ == '__main__':
    main()
