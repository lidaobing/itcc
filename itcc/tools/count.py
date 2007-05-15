# $Id$
def count(ifile, ofile):
    res = {}
    for line in ifile:
        line = line.strip()
        res[line] = res.get(line, 0) + 1
    for x in res:
        ofile.write('%s\t%s\n' % (x, res[x]))

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s <FILE|->\n'
                         % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    count(ifile, sys.stdout)

if __name__ == '__main__':
    main()
