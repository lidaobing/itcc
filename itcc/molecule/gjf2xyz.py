# $Id$

import sys
from itcc.molecule import read, write

__revision__ = '$Rev$'

def gjf2xyz(gjffname, ofile):
    if gjffname == '-':
        ifile = sys.stdin
    else:
        ifile = file(gjffname)
    write.writexyz(read.readgjf(ifile), ofile)
    ofile.close()

def main():
    if len(sys.argv) not in (2, 3):
        import os.path
        print >> sys.stderr, "Usage: %s gjffname|- [xyzfname|-]" % os.path.basename(sys.argv[0])
        sys.exit(1)
    

    if len(sys.argv) == 2 or sys.argv[2] == '-':
        ofile = sys.stdout
    else:
        ofile = file(sys.argv[2], 'w')
    
    gjf2xyz(sys.argv[1], ofile)

if __name__ == '__main__':
    main()




