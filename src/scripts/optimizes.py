#! /usr/bin/env python
import getopt, sys
from itcc.Tinker import tinker

def usage():
    print >> sys.stderr, 'Usage: %s [-c converge] xyzfname ...'

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help"])
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)

    converge = 0.01
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-c"):
            converge = float(a)

    enes = tinker.batchoptimize(args, converge=converge)
    for fname, ene in zip(args, enes):
        print '%s,%.3f' % (fname, ene)
    

    

if __name__ == "__main__":
    main()
