#!/usr/bin/python

import math
from itcc.torsionfit import tools
from itcc.torsionfit import read

def sumxyz(list, filelist):
    if len(list) < 2 or len(list) > 3:
        raise ValueError

    result = []

    for x in filelist:
        mol = read.readxyz(x)
        if len(list) == 2:
            result.append(mol.calclen(list[0], list[1]))
        elif len(list) == 3:
            result.append(math.degrees(mol.calcang(list[0], list[1],
                list[2])))

    print 'n = %d' % len(result)
    print 'average = %f' % tools.average(result)
    print 'stdev = %f' % tools.stdev(result)
    print result
    
def sumxyz_torsion(list, filelist):
    if len(list) != 4:
        raise ValueError

    result = []

    for x in filelist:
        mol = read.readxyz(x)
        result.append(math.degrees(mol.calctor(list[0], list[1],
            list[2], list[3])))

    print 'n = %d' % len(result)

    i = 0
    while i < len(result):
        print '%02i-%02i' % (i+1, i+5), ' '.join(['%7.2f' % x for x in result[i:i+5]])
        i += 5

    dataf = tools.datafreq(result, -180, 180, 36)
    print '\n'.join(['%4d - %4d: %d' % (-180+i*10, -170+i*10, dataf[i]) for i in range(36)])


def main():
    import sys
    import os.path
    if len(sys.argv) >= 3:
        fnamelist = sys.argv[2:]
        atmidx = [int(x) for x in sys.argv[1].split(',')]
        assert 2 <= len(atmidx) <= 4
        if len(atmidx) < 4:
            sumxyz(atmidx, fnamelist)
        else:
            sumxyz_torsion(atmidx, fnamelist)
    else:
        print 'Usage: %s i,j[,k[,l]] filename ...' % \
        os.path.basename(sys.argv[0])
    

if __name__ == '__main__':
    main()       
    
