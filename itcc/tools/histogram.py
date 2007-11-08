# $Id$
import sys
import numpy
import math

try:
    sorted
except:
    from itcc.core.tools import sorted_ as sorted

def histogram(ifile, base, step):
    res = {}
    for line in ifile:
        for word in line.split():
            t = float(word)
            t -= base
            t = int(t//step)
            if t not in res:
                res[t] = 0
            res[t] += 1

    total = 0
    for k, v in sorted(res.items()):
        total += v
        print base + step * k, '~', base + step * (k+1), v, total

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
