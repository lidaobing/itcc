# $Id$

__revision__ = '$Rev$'

import sys
import os.path
import itcc

def help():
    basename = os.path.basename(sys.argv[0])

    print 'Version:', itcc.__version__
    print
    print 'report bugs to <lidaobing@gmail.com>'

def main():
    help()
    
    if len(sys.argv) == 2 and sys.argv[1] == '-v':
        print 'itcc path:', sys.modules['itcc'].__file__
        import numpy
        print 'numpy version:', numpy.__version__

    if len(sys.argv) != 1:
        sys.exit(1)

if __name__ == '__main__':
    main()
