# $Id$

__revision__ = '$Rev$'

from itcc.molecule.read import readxyz
from itcc.molecule.write import writepdb

def xyz2pdb(ifile, ofile):
    writepdb(readxyz(ifile), ofile)

def main():
    import sys
    if len(sys.argv) != 3:
        import os.path
        sys.stderr.write('Usage: %s xyzfile|- pdbfile|-\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)

    if sys.argv[1] == '-':
        ifile = sys.stdin
    else:
        ifile = file(sys.argv[1])

    if sys.argv[2] == '-':
        ofile = sys.stdout
    else:
        ofile = file(sys.argv[2], 'w')

    xyz2pdb(ifile, ofile)

if __name__ == '__main__':
    main()
