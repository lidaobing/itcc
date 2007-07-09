# $Id$
import sys
import math

import numpy

from itcc.molecule import read

def tordiff(mol1, mol2, idxs):
    data1 = numpy.array([mol1.calctor(idx[0], idx[1], idx[2], idx[3]) for idx in idxs])
    data2 = numpy.array([mol2.calctor(idx[0], idx[1], idx[2], idx[3]) for idx in idxs])
    return math.degrees(math.pi - min(abs(abs(data1-data2)-math.pi)))

def main():
    if len(sys.argv) != 5 or sys.argv[1] != '-I':
        import os.path
        sys.stderr.write('Usage: %s -I tor xyzfname1 xyzfname2\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    tor_ifile = sys.stdin
    if sys.argv[2] != '-':
        tor_ifile = file(sys.argv[2])
    tor = [[int(x) - 1 for x in line.split()] for line in tor_ifile.readlines()]
    
    mol1_ifile = sys.stdin
    if sys.argv[3] != '-':
        mol1_ifile = file(sys.argv[3])
    mol1 = read.readxyz(mol1_ifile)
    
    mol2_ifile = sys.stdin
    if sys.argv[4] != '-':
        mol2_ifile = file(sys.argv[4])
    mol2 = read.readxyz(mol2_ifile)
    
    res = tordiff(mol1, mol2, tor)
    print mol1_ifile.name, mol2_ifile.name, res

if __name__ == '__main__':
    main()