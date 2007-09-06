# $Id$

'''convert "1 2\\n3 4\\n" to "1\\n2\\n3\\n4\\n"
'''

__revision__ = '$Rev$'

def onecolumn(ifile, ofile):
    for line in ifile:
        for word in line.split():
            ofile.write("%s\n" % word)

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write(__doc__)
        sys.stderr.write('Usage: %s ifname\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)

    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    onecolumn(ifile, sys.stdout)

if __name__ == '__main__':
    main()
