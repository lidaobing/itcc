#!/usr/bin/env python
# $Id$

import sys
from itcc.Molecule import read, write

__revision__ = '$Rev$'

def gettypes(typefname):
    result = []
    for line in file(typefname):
        types = [int(x) for x in line.split()]
        result.extend(types)
    return result

def settype(xyzfname, typefname):
    mol = read.readxyz(file(xyzfname))
    types = gettypes(typefname)
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
