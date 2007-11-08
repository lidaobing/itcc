# $Id$
import sys
import math
import os.path

import numpy

from itcc.molecule import read

def tordiff(data1, data2, idxs, step=None):
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

def cached_fname2tors(fname, idxs, cache):
    if fname in cache:
        return cache[fname]

    ifile1 = sys.stdin
    if fname != '-':
        ifile1 = file(fname)
    mol1 = read.readxyz(ifile1)
    data1 = numpy.array([mol1.calctor(idx[0], idx[1], idx[2], idx[3]) for idx in idxs])
    cache[fname] = data1
    return data1

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
        files = [tuple(line.split()) for line in file(file_list).readlines()]
    
    cache = {}
    for fname1, fname2 in files:
        tors1 = cached_fname2tors(fname1, tors, cache)
        tors2 = cached_fname2tors(fname2, tors, cache)
            
        res = tordiff(tors1, tors2, step)
        if verbose:
            print fname1, fname2,
        print res

if __name__ == '__main__':
    main()
