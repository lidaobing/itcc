#! /usr/bin/env python
# $Id$
from itcc.CCS2 import loopclosure

__revision__ = '$Rev$'

def testcyc(ifname, options):
    loopc = loopclosure.LoopClosure(options.forcefield,
                                    options.keepbound,
                                    options.searchbound)
    loopc.maxsteps = options.maxsteps
    loopc.moltypekey = options.moltype
    loopc(ifname)

def main():
    from optparse import OptionParser

    usage = "usage: %prog [-h|options] xyzfile"
    parser = OptionParser(usage)
    parser.add_option("-f", "--forcefield", dest='forcefield',
                      default='mm2', help="default is mm2")
    parser.add_option('-k', "--keep", dest="keepbound",
                      default=None, type='float',
                      help='keep boundary(kcal/mol), default is no boundary')
    parser.add_option('-s', "--search", dest="searchbound",
                      default=None, type='float',
                      help='search boundary(kcal/mol), default is no boundary')
    parser.add_option('-m', "--maxsteps", dest="maxsteps",
                      default=0, type='int',
                      help='max optimization steps, default is infinite')
    parser.add_option('-t', "--moltype", dest="moltype",
                      default=None, help='you can set it to peptide')
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    testcyc(args[0], options)

if __name__ == '__main__':
    main()

