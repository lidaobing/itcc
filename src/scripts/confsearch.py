#! /usr/bin/python
# $Id$
from itcc.CCS2 import loopclosure, R6combine

__revision__ = '$Rev$'

def testcyc(ifname, options):
    combine_dict = {1:R6combine.R6combine1,
                    2:R6combine.R6combine2,
                    3:R6combine.R6combine3}
    loopc = loopclosure.LoopClosure(options.forcefield,
                                    options.keepbound,
                                    options.searchbound)
    loopc.maxsteps = options.maxsteps
    loopc.f_R6combine = combine_dict[options.combine]
    
    loopc(ifname)

def main():
    from optparse import OptionParser

    usage = "usage: %prog [options] xyzfile"
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
    parser.add_option('-c', "--combine", dest="combine",
                      default=3, type='int',
                      help='-c1: Comb I, -c2: Comb II, -c3: Comb III, '
                      'default: -c3') 
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    testcyc(args[0], options)    

if __name__ == '__main__':
    main()
        
