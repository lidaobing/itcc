# $Id$

from itcc.Tinker import tinker

__revision__ = '$Rev$'

def main():
    import sys
    if 2 <= len(sys.argv) <= 3:
        lines = tinker.constrain(*(sys.argv[1:]))
        for x in lines:
            print x,
    else:
        print >> sys.stderr, 'Usage: %s xyzfname [param]' % sys.argv[0]

if __name__ == '__main__':
    main()
