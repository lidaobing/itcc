#!/usr/bin/env python

from itcc.Torsionfit import parmfit

def main():
    import sys
    if len(sys.argv) != 4:
        import os.path
        print >> sys.stderr, 'Usage: %s datfname idxfname param' % \
              os.path.basename(sys.argv[0])
        sys.exit(1)
    parmfit.parmfit(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()
