#! /usr/bin/env python

from itcc.torsionfit import read, write

def gjf2xyz(gjffname, xyzfname):
    write.writexyz(read.readgjf(gjffname), xyzfname)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: %s gjffname xyzfname" % sys.argv[0]
    else:
        gjf2xyz(sys.argv[1], sys.argv[2])




