# $Id$

__revision__ = '$Rev$'

import sys
from itcc.molecule import read
from itcc.molecule.relalist import Relalist
from itcc.tools.tools import all

def mol2top(molfname, ofile=sys.stdout):
    if(not hasattr(molfname, 'read')):
      ifile = file(molfname)
    else:
      ifile = molfname
    mol = read.readxyz(ifile)
    tors = Relalist(mol).torsions
    for tor in tors:
        if all([mol.atoms[idx].type != 5 for idx in tor]):
            ofile.write('%s\n' % ' '.join([str(idx+1) for idx in tor]))

def main():
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write("output all the torsions(except the torsion "
                         "include H), we assume H's type is 5\n") 
        sys.stderr.write("Usage: %s xyzfname\n" % sys.argv[0])
        sys.exit(1)

    mol2top(sys.argv[1])

if __name__ == '__main__':
    main()
