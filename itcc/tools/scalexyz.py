# $Id$

__revision__ = '$Rev$'

from itcc.Molecule import read, write

def scalexyz(ifname, scaleratio):
    mol = read.readxyz(file(ifname))
    mol.coords = [coord * scaleratio for coord in mol.coords]
    write.writexyz(mol)

def main():
    import sys
    if len(sys.argv) != 3:
        print >> sys.stderr, 'Usage: %s xyzfname scaleratio' % sys.argv[0]
        sys.exit(1)

    scalexyz(sys.argv[1], float(sys.argv[2]))

if __name__ == '__main__':
    main()
