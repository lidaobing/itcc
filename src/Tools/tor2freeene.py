# $Id$
import math
import sys
import getopt

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

def tor2freeene2(ifname, column, countnum, temperature):
    R = 8.314e-3 / 4.184                   # kcal/K*mol
    datas = []

    for line in file(ifname):
        datas.append(float(line.split()[column]))

    datas.sort()

    assert len(datas) >= countnum

    breaks = []

    for idx in range(countnum+1):
        breakidx = idx * len(datas) / countnum
        if idx == 0:
            breakvalue = datas[0]
        elif idx == countnum:
            breakvalue = datas[-1]
        else:
            breakvalue = (datas[breakidx-1]+datas[breakidx])/2.0
        breaks.append(breakvalue)

    lens = []
    centers = []
    for idx in range(countnum):
        lens.append(breaks[idx+1] - breaks[idx])
        centers.append((breaks[idx+1] + breaks[idx])/2.0)

    minlen = min(lens)
    for idx in range(countnum):
        print centers[idx], R*temperature*math.log(lens[idx]/minlen)

def usage(ofile=sys.stderr):
    import os.path
    print >> ofile, 'Usage: %s [-n] filename [column [count [temperature]]]' % \
          os.path.basename(sys.argv[0])
    print >> ofile
    print >> ofile, '-n   new mode'
    print >> ofile, 'default column is 1(first column)'
    print >> ofile, 'default count is 36'
    print >> ofile, 'default temperature is 300K'

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn", ["newmode", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    count = 36
    temperature = 300.0
    column = 0
    mode = tor2freeene

    for o, a in opts:
        if o in ("-h", "--help"):
            usage(sys.stdout)
            sys.exit()
        elif o in ('-n', '--newmode'):
            mode = tor2freeene2

    if not 1 <= len(args) <= 4:
        usage()
        sys.exit(2)
    ifname = args[0]

    if len(args) >= 2:
        column = int(args[1]) - 1
    if len(args) >= 3:
        count = int(args[2])
    if len(args) >= 4:
        temperature = float(args[3])

    mode(ifname, column, count, temperature)

if __name__ == '__main__':
    main()
