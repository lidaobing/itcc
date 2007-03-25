# $Id$

__revision__ = '$Rev$'

import sys
from itcc.molecule import read, write

def xyz2gjf(xyzfname):
    write.writegjf(read.readxyz(file(xyzfname)), sys.stdout)

def main():
    if len(sys.argv) != 2:
        import os.path
        print >> sys.stderr, 'Usage: %s xyzfname' % \
            os.path.basename(sys.argv[0])
        sys.exit(1)
    else:
        xyz2gjf(sys.argv[1])

if __name__ == '__main__':
    main()

