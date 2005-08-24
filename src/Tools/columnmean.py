# $Id$

__revision__ = '$Rev$'

def columnmean(ifile):
    line = ifile.readline()
    totals = [float(word) for word in line.split()]
    linecount = 1

    for line in ifile:
        words = line.split()
        assert len(words) == len(totals)
        totals = [total + float(word) for total, word in zip(totals, words)]
        linecount += 1

    totals = [total/linecount for total in totals]
    print '\t'.join([str(total) for total in totals])

def main():
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s {ifname|-}\n' % sys.argv[0])
        sys.exit(1)

    if sys.argv[1] == '-':
        ifile = sys.stdin
    else:
        ifile = file(sys.argv[1])
    columnmean(ifile)

if __name__ == '__main__':
    main()
