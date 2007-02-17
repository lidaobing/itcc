# $Id$

def almost_equal_diff(ifile1, ifile2, diff):
    line1 = ifile1.readline()
    line2 = ifile2.readline()
    d1 = float(line1)
    d2 = float(line2)
    while 1:
        if not line1 or not line2: break
        if abs(d1 - d2) <= diff:
            line1 = ifile1.readline()
            line2 = ifile2.readline()
            if line1: d1 = float(line1)
            if line2: d2 = float(line2)
        elif d1 > d2:
            print '> %s' % line2,
            line2 = ifile2.readline()
            if line2: d2 = float(line2)
        else:
            print '< %s' % line1,
            line1 = ifile1.readline()
            if line1: d1 = float(line1)
    if line1:
        print '< %s' % line1,
    if line2:
        print '> %s' % line2,
    for line in ifile1:
        print '< %s' % line,
    for line in ifile2:
        print '> %s' % line,

def main():
    import sys
    if len(sys.argv) != 5 or sys.argv[1] != "-d":
        import os.path
        sys.stderr.write('Usage: %s -d DIFF FILE1|- FILE2|-\n'
                           % os.path.basename(sys.argv[0]))
        sys.exit(1)
    if sys.argv[3] == '-':
        ifile1 = sys.stdin
    else:
        ifile1 = file(sys.argv[3])

    if sys.argv[4] == '-':
        ifile2 = sys.stdin
    else:
        ifile2 = file(sys.argv[4])

    almost_equal_diff(ifile1,
                      ifile2,
                      float(sys.argv[2]))

if __name__ == '__main__':
    main()
