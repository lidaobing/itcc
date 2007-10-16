# $Id$

def scanlog2enestep(ifile, ofile):
    step = 0
    for line in ifile:
        if 'Step' in line:
            step += 1
        elif 'Potential Surface Map' in line:
            ofile.write('%s %i\n' % (line.split()[-1], step))

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write(
            'Usage: %s [-i] <ifname|->\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)

    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    
    scanlog2enestep(ifile, sys.stdout)

if __name__ == '__main__':
    main()
