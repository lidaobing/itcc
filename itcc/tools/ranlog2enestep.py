# $Id$

def ranlog2enestep(ifile, ofile):
    cache = set()
    for idx, line in enumerate(ifile):
        enestr = line.split()[-1]
        if enestr not in cache:
            cache.add(enestr)
            ofile.write('%s %s\n' % (enestr, idx+1))

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s FILE|-\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    
    ranlog2enestep(ifile, sys.stdout)

if __name__ == '__main__':
    main()