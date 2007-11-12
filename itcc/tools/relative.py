# $Id$

import sys

from itcc.core import IgnoreEpipe

def relative(ifile, ofile, verbose, base=None, number=False):
    data = []
    for line in ifile:
        for word in line.split():
            data.append(float(word))
    
    if base is None:
        base = min(data)
        
    idx = 1
    
    for x in data:
        if number:
            ofile.write('%i\t' % idx)
            idx += 1
        if verbose:
            ofile.write('%f\t%f\n' % (x, x-base))
        else:
            ofile.write('%f\n' % (x-base))

def main():
    verbose = False
    base = None
    number = False
    
    import getopt
    opts, args = getopt.getopt(sys.argv[1:], "vnb:")
    
    for k, v in opts:
        if k == '-v':
            verbose = True
        elif k == '-b':
            base = float(v)
        elif k == '-n':
            number = True
            
    if len(args) != 1:
        import os.path
        sys.stderr.write('Usage: %s [-v] [-n] [-b base] <FILE|->\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    ifile = sys.stdin
    if args[0] != '-':
        ifile = file(args[0])
    
    ofile = IgnoreEpipe(sys.stdout)
    
    relative(ifile, ofile, verbose, base, number)

if __name__ == '__main__':
    main()
