# $Id$

import sys

def pdbqcharge(ifile, ofile, verbose):
    result = 0.0
    
    for line in ifile:
        words = line.split()
        if words and words[0] in ('ATOM', 'HEATM'):
            charge = float(line[70:76])
            result += charge
            if verbose:
                print line[6:11], line[70:76]
    
    if verbose:
        print 'charge sum'
    print '%.3f' % result

def usage(ofile):
    import os.path
    ofile.write('Usage: %s [-v] <pdbqfile|->\n'
                % os.path.basename(sys.argv[0]))

def main():
    verbose = False
    
    args = sys.argv[1:]
    
    if args and args[0] == '-v':
        verbose = True
        args = args[1:]
        
    if len(args) != 1:
        usage(sys.stderr)
        sys.exit(1)
    
    ifile = sys.stdin
    if args[0] != '-':
        ifile = file(args[0])
        
    pdbqcharge(ifile, sys.stdout, verbose)

if __name__ == '__main__':
    main()