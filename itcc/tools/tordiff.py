# $Id$
import sys
import math
import os.path

import numpy

from itcc.molecule import read

def tordiff(mol1, mol2, idxs, step=None):
    data1 = numpy.array([mol1.calctor(idx[0], idx[1], idx[2], idx[3]) for idx in idxs])
    data2 = numpy.array([mol2.calctor(idx[0], idx[1], idx[2], idx[3]) for idx in idxs])
    if step is None:
        data2s = [data2]
    else:
        data2s = [data2.take(tuple(range(i,len(data2))+range(i)), axis=0) 
                  for i in range(0, len(data2), step)]
    return math.degrees(min([math.pi - min(abs(abs(data1-x)-math.pi)) 
                             for x in data2s]))

def usage(ofile):
    usage = 'Usage:\n'
    usage += '  %s [options] -I tor fname1 fname2\n' % os.path.basename(sys.argv[0])
    usage += '  %s [options] -F fname -I tor\n' % os.path.basename(sys.argv[0])
    usage += '\n'
    usage += 'Options:\n'
    usage += '  -s  logical symmetry: step\n'
    usage += '  -v  verbose\n'
    ofile.write(usage)

def main():
    import getopt
    opts, args = getopt.getopt(sys.argv[1:], "vI:s:F:")
    
    tor = None
    step = None
    file_list = None
    verbose = False
    
    for k, v in opts:
        if k == '-I':
            tor = v
        elif k == '-s':
            step = int(v)
        elif k == '-F':
            file_list = v
        elif k == '-v':
            verbose = True
    
    if tor is None \
        or (file_list is None and len(args) != 2) \
        or (file_list is not None and len(args) != 0):
        usage(sys.stderr)
        sys.exit(1)
    
    tor_ifile = sys.stdin
    if tor != '-':
        tor_ifile = file(tor)
    tors = [[int(x)-1 for x in line.split()] for line in tor_ifile.readlines()]
    
    if file_list is None:
        files = [tuple(args)]
    else:
        files = [tuple(line.split()) for line in file_list.readlines()]
    
    for fname1, fname2 in files:
        ifile1 = sys.stdin
        if fname1 != '-':
            ifile1 = file(fname1)
        mol1 = read.readxyz(ifile1)
        
        ifile2 = sys.stdin
        if fname2 != '-':
            ifile2 = file(fname2)
        mol2 = read.readxyz(ifile2)
            
        res = tordiff(mol1, mol2, tors, step)
        if verbose:
            print ifile1.name, ifile2.name,
        print res

if __name__ == '__main__':
    main()