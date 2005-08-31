# $Id$

__revision__ = '$Rev$'

def onecolumn(ifname):
    for line in file(ifname):
        for word in line.split():
            print word

def main():
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s ifname\n' % sys.argv[0])
        sys.exit(1)
    onecolumn(sys.argv[1])

if __name__ == '__main__':
    main()
