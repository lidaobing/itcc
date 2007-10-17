# $Id$

def omega2restrain(ifile, ofile):
    for line in ifile:
        line = line.strip()
        assert len(line.split()) == 4
        ofile.write('RESTRAIN-TORSION %s 1.0 120.0 240.0\n' % line)

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s OMEGA|-\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
        
    omega2restrain(ifile, sys.stdout)

if __name__ == '__main__':
    main()
