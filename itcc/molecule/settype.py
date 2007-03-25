# $Id$

import sys
from itcc.molecule import read, write

__revision__ = '$Rev$'

def _gettypes(typefile):
    for line in typefile:
        for word in line.split():
            yield int(word)

def settype(xyzfile, typefile):
    mol = read.readxyz(xyzfile)
    types = tuple(_gettypes(typefile))
    assert len(mol) == len(types), "%s - %s" % (len(mol), len(types))
    for idx, atype in enumerate(types):
        mol.settype(idx, atype)
    write.writexyz(mol, sys.stdout)

def main():
    if len(sys.argv) != 3:
        import os.path
        print >> sys.stderr, "Usage: %s {XYZFNAME|-} {TYPEFNAME|-}" % \
              os.path.basename(sys.argv[0])
        sys.exit(1)
    if sys.argv[1] == '-':
        xyzfile = sys.stdin
    else:
        xyzfile = file(sys.argv[1])

    if sys.argv[2] == '-':
        typefile = sys.stdin
    else:
        typefile = file(sys.argv[2])
    settype(xyzfile, typefile)

if __name__ == '__main__':
    main()
