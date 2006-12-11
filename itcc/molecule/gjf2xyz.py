# $Id$

import sys
from itcc.molecule import read, write

__revision__ = '$Rev$'

def gjf2xyz(gjffname, xyzfname):
    ofile = file(xyzfname, 'w')
    if gjffname == '-':
        ifile = sys.stdin
    else:
        ifile = file(gjffname)
    write.writexyz(read.readgjf(ifile), ofile)
    ofile.close()

def main():
    import sys
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: %s gjffname|- xyzfname" % sys.argv[0]
        sys.exit(1)

    gjf2xyz(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()




