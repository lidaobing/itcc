#! /usr/bin/env python
# $Id$

from itcc.Molecule import read, write

__revision__ = '$Rev$'

def gjf2xyz(gjffname, xyzfname):
    ofile = file(xyzfname, 'w+')
    write.writexyz(read.readgjf(gjffname), ofile)
    ofile.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: %s gjffname xyzfname" % sys.argv[0]
    else:
        gjf2xyz(sys.argv[1], sys.argv[2])




