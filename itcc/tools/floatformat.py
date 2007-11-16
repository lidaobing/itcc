# $Id$

def floatformat(ifile, ofile, format):
    for line in ifile:
        words = line.split()
        res = []
        for x in words:
            try:
                x2 = format % float(x)
            except ValueError:
                x2 = x
            res.append(x2)
        ofile.write(' '.join(res) + '\n')

def main():
    import sys
    if len(sys.argv) not in (2, 3):
        import os.path
        sys.stderr.write('Usage: %s <FNAME> [FORMAT]\n'
                         ' default format is "%.0f"' % os.path.basename(sys.argv[0]))
        sys.exit(1)

    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])

    format = '%.0f'
    if len(sys.argv) >= 3:
        format = sys.argv[2]

    floatformat(ifile, sys.stdout, format)

if __name__ == '__main__':
    main()
