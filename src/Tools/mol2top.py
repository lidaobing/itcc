# $Id$

__revision__ = '$Rev$'

from itcc.Molecule import read
from itcc.Molecule.relalist import Relalist
from itcc.Tools.tools import all

def mol2top(molfname):
    mol = read.readxyz(file(molfname))
    tors = Relalist(mol).torsions
    for tor in tors:
        if all([mol.atoms[idx].type != 5 for idx in tor]):
            print ' '.join([str(idx+1) for idx in tor])

def main():
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: %s xyzfname\n" % sys.argv[0])
        sys.exit(1)

    mol2top(sys.argv[1])

if __name__ == '__main__':
    main()