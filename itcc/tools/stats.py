# $Id$
# pylint: disable-msg=W0401
# pylint: disable-msg=W0611
# pylint: disable-msg=W0622

__revision__ = '$Rev$'

from numpy import *

def stat_helper(ifile):
    for line in ifile:
        for word in line.split():
            yield float(word)

def stat(ifile):
    data = array(tuple(stat_helper(ifile)))
    print 'n', len(data)
    print 'sum', data.sum()
    if len(data) == 0:
        return
    print 'min', data.min()
    print 'max', data.max()
    print 'median', median(data)
    print 'mean', data.mean()
    print 'stdev', data.std()

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write("Usage: %s datafile|-\n"
                         % os.path.basename(sys.argv[0]))
        sys.exit(1)
    if sys.argv[1] == '-':
        stat(sys.stdin)
    else:
        stat(file(sys.argv[1]))

if __name__ == '__main__':
    main()
