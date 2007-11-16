# $Id$

def loop2looptor(ifile, ofile, l=4):
    a = [int(x) for x in ifile.read().split()]
    a = a[-1:] + a[:-1]
    a += a
    formatstr = ('%i ' * l)[:-1] + '\n'
    for i in range(len(a)/2):
        ofile.write(formatstr % tuple(a[i:i+l]))

def main():
    import sys
    import getopt
    
    opts, args = getopt.getopt(sys.argv[1:], 'l:')

    if len(args) != 1:
        import os.path
        sys.stderr.write('Usage: %s [-l N] <loop|->\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)

    l = 4
    for k, v in opts:
        if k == '-l':
            l = int(v)

    ifile = sys.stdin
    if args[0] != '-':
        ifile = file(args[0])
    loop2looptor(ifile, sys.stdout, l)

if __name__ == '__main__':
    main()
