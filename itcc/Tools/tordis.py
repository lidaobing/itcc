# $Id$

__revision__ = '$Rev$'

import math

def normtor(tor, lower=-180.0, upper=180.0):
    return (tor - lower) % (upper - lower) + lower

def tordis(ifname):
    ifile = file(ifname)
    headline = ifile.readline()
    basetors = [float(x) for x in headline.split()]
    colnum = len(basetors)

    print 0.0

    for line in ifile:
        tors = [float(x) for x in line.split()]
        assert len(tors) == colnum
        difftors = [normtor(tor1-tor2) for tor1, tor2 in zip(tors, basetors)]
        tordiff = math.sqrt(sum([tor*tor for tor in difftors]))
        print tordiff

    ifile.close()

def main():
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s torfname\n' % sys.argv[0])
        sys.exit(1)
    tordis(sys.argv[1])

if __name__ == '__main__':
    main()
