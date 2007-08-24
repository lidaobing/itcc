# $Id$

import sys

def relative(ifile, ofile, verbose, base=None):
    data = []
    for line in ifile:
        for word in line.split():
            data.append(float(word))
    
    if base is None:
        m = min(data)
    
    try:
        for x in data:
            if verbose:
                ofile.write('%f\t%f\n' % (x, x-base))
            else:
                ofile.write('%f\n' % (x-base))
    except IOError, e:
        import errno
        if e.errno != errno.EPIPE:
            raise

def main():
    verbose = False
    base = None
    
    import getopt
    opts, args = getopt.getopt(sys.argv[1:], "vb:")
    
    for k, v in opts:
        if k == '-v':
            verbose = True
        elif k == '-b':
            base = float(v)
            
    if len(args) != 1:
        import os.path
        sys.stderr.write('Usage: %s [-v] [-b base] <FILE|->\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    ifile = sys.stdin
    if args[0] != '-':
        ifile = file(args[0])
    
    ofile = sys.stdout
    
    relative(ifile, ofile, verbose, base)

if __name__ == '__main__':
    main()
