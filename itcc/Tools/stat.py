# $Id$

__revision__ = '$Rev$'

from scipy import stats

def stat_helper(ifile):
    for line in ifile:
        yield float(line)

def stat(ifile):
    data = tuple(stat_helper(ifile))
    print 'mean=%s' % stats.mean(data),
    print 'std=%s' % stats.std(data)

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
