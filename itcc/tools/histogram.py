# $Id$
import sys
import numpy

def histogram(ifile, base, step):
    data = numpy.array([float(x) for x in ifile.read().split()])
    data -= base
    data /= step
    data = numpy.floor(data)

    res = {}
    for x in data:
        if x not in res:
            res[x] = 0
        res[x] += 1

    for k, v in sorted(res.items()):
        print base + step * k, '~', base + step * (k+1), v

def usage(ofile):
    import os.path
    ofile.write('Usage: %s <file|-> base step\n' % os.path.basename(sys.argv[0]))

def main():
    if len(sys.argv) != 4:
        usage(sys.stderr)
        sys.exit(1)

    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])

    base = float(sys.argv[2])
    step = float(sys.argv[3])
    histogram(ifile, base, step)

if __name__ == '__main__':
    main()
