# $Id$

def ene2agr(ifiles, ofile):
    i1 = 0
    for idx, ifile in enumerate(ifiles):
        data = [float(x) for x in ifile]
        data_min = min(data)
        for x in data:
            ofile.write('@    s%i line color %i\n' % (i1, idx+1))
            ofile.write('@target G0.S%i\n' % i1)
            ofile.write('@type xy\n')
            ofile.write('%i %s\n' % (idx*2+1, x - data_min))
            ofile.write('%i %s\n' % (idx*2+2, x - data_min))
            ofile.write('&\n')
            i1 += 1

def main():
    import sys
    if len(sys.argv) < 2:
        import os.path
        sys.stderr.write("Usage: %s FILE|- ...\n" % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ifiles = []
    for x in sys.argv[1:]:
        if x == '-':
            ifiles.append(sys.stdin)
        else:
            ifiles.append(file(x))
    ene2agr(ifiles, sys.stdout)

if __name__ == '__main__':
    main()
