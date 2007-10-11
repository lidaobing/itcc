# $Id$

import sys
import os.path

def tor2omega(ifile, ofile):
    for line in ifile:
        data = [float(x) for x in line.split()]
        res = []
        for x in data:
            if abs(x) > 90:
                res.append('T')
            else:
                res.append('C')
        ofile.write(''.join(res)+'\n')

def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s FILE\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    
    tor2omega(ifile, sys.stdout)

if __name__ == '__main__':
    main()