# $Id$

import sys
from itcc.molecule import read, write

__revision__ = '$Rev$'

def gettypes(typefname):
    for line in file(typefname):
        for word in line.split():
            yield int(word)

def settype(xyzfname, typefname):
    mol = read.readxyz(file(xyzfname))
    types = tuple(gettypes(typefname))
    assert len(mol) == len(types)
    for idx, atype in enumerate(types):
        mol.settype(idx, atype)
    write.writexyz(mol, sys.stdout)

def main():
    if len(sys.argv) != 3:
        import os.path
        print >> sys.stderr, "Usage: %s xyzfname typefname" % \
              os.path.basename(sys.argv[0])
        sys.exit(1)
    settype(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
