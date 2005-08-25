# $Id$

__revision__ = '$Rev$'

def columnmean(ifile, input_header, output_header):
    if input_header:
        header = ifile.readline()
        if output_header:
            print header.strip()

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
    from optparse import OptionParser

    usage = 'usage: %prog [-h|options] {ifname|-}'
    parser = OptionParser(usage)
    parser.add_option('-i', '--input-header',
                      action='store_true', dest='input_header',
                      help='input file has header')
    parser.add_option('-o', '--output-header',
                      action='store_true', dest='output_header',
                      help='output header')
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("incorrect number of arguments")

    if args[0] == '-':
        ifile = sys.stdin
    else:
        ifile = file(args[0])

    columnmean(ifile, options.input_header, options.output_header)

if __name__ == '__main__':
    main()
