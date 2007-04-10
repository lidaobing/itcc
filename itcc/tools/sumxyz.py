# $Id$

import math
import sys

from Scientific import Statistics

from itcc.tools import tools
from itcc.molecule import read

__revision__ = '$Rev$'

def sumxyz(seq, filelist):
    if len(seq) < 2 or len(seq) > 3:
        raise ValueError

    result = []

    for x in filelist:
        if x == '-':
            ifile = sys.stdin
        else:
            ifile = file(x)
        mol = read.readxyz(ifile)
        if len(seq) == 2:
            result.append(mol.calclen(seq[0], seq[1]))
        elif len(seq) == 3:
            result.append(math.degrees(mol.calcang(seq[0], seq[1],
                                                   seq[2])))

    print 'n = %d' % len(result)
    print 'average = %f' % Statistics.mean(result)
    if len(filelist) >= 2:
        print 'stdev = %f' % Statistics.standardDeviation(result)
    print result

def sumxyz_torsion(list_, filelist):
    if len(list_) != 4:
        raise ValueError

    result = []

    for x in filelist:
        if x == '-':
            ifile = sys.stdin
        else:
            ifile = file(x)
        mol = read.readxyz(ifile)
        result.append(math.degrees(mol.calctor(list_[0], list_[1],
            list_[2], list_[3])))

    print 'n = %d' % len(result)

    i = 0
    while i < len(result):
        print '%02i-%02i' % (i+1, i+5),
        print ' '.join(['%7.2f' % x for x in result[i:i+5]])
        i += 5

    dataf = tools.datafreq(result, -180, 180, 36)
    print '\n'.join(['%4d - %4d: %d' % (-180+i*10, -170+i*10, dataf[i])
                     for i in range(36)])


def main():
    import os.path
    if len(sys.argv) < 3:
        sys.stderr.write('Usage: %s i,j[,k[,l]] filename ...\n' % \
                           os.path.basename(sys.argv[0]))
        sys.stderr.write('  index begin with 1\n')
        sys.exit(1)
    fnamelist = sys.argv[2:]
    atmidx = [int(x)-1 for x in sys.argv[1].split(',')]
    assert 2 <= len(atmidx) <= 4
    if len(atmidx) < 4:
        sumxyz(atmidx, fnamelist)
    else:
        sumxyz_torsion(atmidx, fnamelist)


if __name__ == '__main__':
    main()
