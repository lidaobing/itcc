# $Id$

from itcc.tinker import tinker

__revision__ = '$Rev$'

def main():
    import sys
    if 2 <= len(sys.argv) <= 3:
        lines = tinker.constrain(*(sys.argv[1:]))
        for x in lines:
            print x,
    else:
        import os.path
        print >> sys.stderr, 'Usage: %s xyzfname [param]' % os.path.basename(sys.argv[0])
        sys.exit(1)

if __name__ == '__main__':
    main()
