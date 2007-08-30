# $Id$

def ccslog2enestep(ifile, ofile):
    step = 0
    for line in ifile:
        if line.startswith("  Step"):
            step = int(line.split()[1])
        elif line.startswith("    Potential"):
            ofile.write("%s %s\n" % (line.split()[-1], step))

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s ifile > ofile\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ccslog2enestep(file(sys.argv[1]), sys.stdout)    

if __name__ == '__main__':
    main()
    
