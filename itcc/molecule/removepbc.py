# $Id$

__revision__ = '$Rev$'

from itcc.molecule import write, molecule, mtxyz

def nearestmirror(coord, origin, pbc):
    result = [None] * 3
    for i in range(3):
        result[i] = (coord[i] - origin[i]) % pbc[i]
        if result[i] > pbc[i] / 2.0:
            result[i] -= pbc[i]
        result[i] += origin[i]
    return molecule.CoordType(result)

def removepbc(xyzfname, pbc):
    for mol in mtxyz.Mtxyz(file(xyzfname)):
        coords = mol.coords
        origin = coords[0]
        for i in range(1, len(coords)):
            coords[i] = nearestmirror(coords[i], origin, pbc)
        write.writexyz(mol)

def main():
    import sys
    if len(sys.argv) not in (3, 5):
        import os.path
        basename = os.path.basename(sys.argv[0])
        sys.stderr.write('Usage: %s xyzfname pbc.x\n' % basename)
        sys.stderr.write('       %s xyzfname pbc.x pbc.y pbc.z\n' % basename)
        sys.exit(1)
    if len(sys.argv) == 3:
        removepbc(sys.argv[1], [float(sys.argv[2])] * 3)
    else:
        removepbc(sys.argv[1], [float(x) for x in sys.argv[2:5]])

if __name__ == '__main__':
    main()
