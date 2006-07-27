# $Id$

from itcc.molecule import read, write

__revision__ = '$Rev$'

def gjf2xyz(gjffname, xyzfname):
    ofile = file(xyzfname, 'w+')
    write.writexyz(read.readgjf(gjffname), ofile)
    ofile.close()

def main():
    import sys
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: %s gjffname xyzfname" % sys.argv[0]
        sys.exit(1)

    gjf2xyz(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()




