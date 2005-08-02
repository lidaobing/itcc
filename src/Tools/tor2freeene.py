# $Id$
import math

__revision__ = '$Rev$'

def tor2freeene(ifname, column, countnum, temperature):
    R = 8.314e-3 / 4.184                   # kcal/K*mol

    counts = [0] * (countnum + 1)
    base = -180.0 / countnum - 180.0
    interval = 360.0 / countnum
    for line in file(ifname):
        data = float(line.split()[column])
        idx = int((data - base) / interval)
        counts[idx] += 1
    counts[0] += counts[-1]
    counts[-1] = counts[0]

    zerocount = float(max(counts))
    G = []
    for count in counts:
        if count == 0:
            G.append('N/A')
            continue
        G.append(-R*temperature*math.log(count/zerocount))

    for i in range(len(counts)):
        print -180.0 + i * interval, counts[i], G[i]

def main():
    import sys

    count = 36
    temperature = 300.0
    column = 0

    if not 2 <= len(sys.argv) <= 5:
        import os.path
        print >> sys.stderr, 'Usage: %s filename [column [count [temperature]]]' % \
              os.path.basename(sys.argv[0])
        print >> sys.stderr
        print >> sys.stderr, 'default column is 1(first column)'
        print >> sys.stderr, 'default count is %i' % count
        print >> sys.stderr, 'default temperature is %.0fK' % temperature
        sys.exit(1)
    ifname = sys.argv[1]

    if len(sys.argv) >= 3:
        column = int(sys.argv[2]) - 1
    if len(sys.argv) >= 4:
        count = int(sys.argv[3])
    if len(sys.argv) >= 5:
        temperature = float(sys.argv[4])

    tor2freeene(ifname, column, count, temperature)


if __name__ == '__main__':
    main()
