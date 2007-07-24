# $Id$

__revision__ = '$Rev$'

import sys
from itcc.molecule import read
from itcc.molecule.relalist import Relalist
from itcc.core.tools import all

def mol2tor(molfname, ofile=sys.stdout):
    if(not hasattr(molfname, 'read')):
      ifile = file(molfname)
    else:
      ifile = molfname
    mol = read.readxyz(ifile)
    tors = Relalist(mol).torsions
    for tor in tors:
        if all([mol.atoms[idx].no != 1 for idx in tor]):
            ofile.write('%s\n' % ' '.join([str(idx+1) for idx in tor]))

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write("output all the torsions(except the torsion "
                         "include H)\n") 
        sys.stderr.write("Usage: %s xyzfname\n" % os.path.basename(sys.argv[0]))
        sys.exit(1)

    mol2tor(sys.argv[1])

if __name__ == '__main__':
    main()
