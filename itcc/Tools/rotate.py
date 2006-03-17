# $Id$

__revision__ = '$Rev$'

def rotate(minval, maxval, ifile):
    for line in ifile:
        words = line.split()
        for x in words:
            print (float(x) - minval) % (maxval - minval) + minval,
        print

def main():
    import sys
    if len(sys.argv) != 4:
        import os.path
        sys.stderr.write('Usage: %s min max datafile|-\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    if sys.argv[3] == '-':
        rotate(float(sys.argv[1]), float(sys.argv[2]), sys.stdin)
    else:
        rotate(float(sys.argv[1]), float(sys.argv[2]), file(sys.argv[3]))

if __name__ == '__main__':
    main()
