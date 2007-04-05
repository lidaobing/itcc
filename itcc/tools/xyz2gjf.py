# $Id$

__revision__ = '$Rev$'

import sys
from itcc.molecule import read, write

def xyz2gjf(ifile, header = None):
    write.writegjf(read.readxyz(ifile), sys.stdout, header)

def _usage(ofile):
    ofile.write('Usage: xyz2gjf [-h <headerfile|->] <xyzfname|->\n')

def main():
    argv = sys.argv[1:]
    headerfname = None
    if argv:
        if argv[0] == '-h':
            argv = argv[1:]
            if not argv:
                _usage(sys.stderr)
                sys.exit(1)
            headerfname = argv[0]
            argv = argv[1:]
    if len(argv) != 1:
        _usage(sys.stderr)
        sys.exit(1)

    header = None
    if headerfname is not None:
        if headerfname == '-':
            header = sys.stdin.read()
        else:
            header = file(headerfname).read()

    if argv[0] == '-':
        ifile = sys.stdin
    else:
        ifile = file(argv[0])
    xyz2gjf(ifile, header)

if __name__ == '__main__':
    main()

