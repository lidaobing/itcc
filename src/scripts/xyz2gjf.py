#! /usr/bin/env python
# $Id$

__revision__ = '$Rev$'

import sys
from itcc.Molecule import read, write

def xyz2gjf(xyzfname):
    write.writegjf(read.readxyz(file(xyzfname)), sys.stdout)

def main():
    if len(sys.argv) != 2:
        import os.path
        print >> sys.stderr, 'Usage %s xyzfname' % \
            os.path.basename(sys.argv[0])
    else:
        xyz2gjf(sys.argv[1])

if __name__ == '__main__':
    main()

