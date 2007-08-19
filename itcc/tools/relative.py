# $Id$

import sys

def relative(ifile, ofile, verbose):
    data = []
    for line in ifile:
        for word in line.split():
            data.append(float(word))
    
    m = min(data)
    
    try:
        for x in data:
            if verbose:
                ofile.write('%f\t%f\n' % (x, x-m))
            else:
                ofile.write('%f\n' % (x-m))
    except IOError, e:
        import errno
        if e.errno != errno.EPIPE:
            raise

def main():
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s [-v] <FILE|->\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    args = sys.argv[1:]
    
    verbose = False
    if args and args[0] == '-v':
        verbose = True
        args = args[1:]
        
    if len(args) != 1:
        import os.path
        sys.stderr.write('Usage: %s [-v] <FILE|->\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    
    ofile = sys.stdout
    
    relative(ifile, ofile, verbose)

if __name__ == '__main__':
    main()
