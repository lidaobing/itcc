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

if __name__ == '__main__':
    main()
