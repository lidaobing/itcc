#! /usr/bin/python
# $Id$
import math
import os.path
import time
import resource
from itcc.CCS2 import loopclosure, loopdetect
from itcc.Molecule import readxyz, writexyz
from itcc.Tinker import tinker
from itcc.CCS2 import neighbour, R6combine

__revision__ = '$Rev$'

def statstor(mol):
    loops = loopdetect(mol)
    assert len(loops) == 1
    loop = loops[0]
    doubleloop = loop * 2
    tors = [math.degrees(mol.calctor(*doubleloop[i:i+4]))
            for i in range(len(loop))]
    return tors

def testcyc(ifname, options):
    neighbour_dict = {1:neighbour.NeighbourI,
                      2:neighbour.NeighbourII}
    combine_dict = {1:R6combine.R6combine1,
                    2:R6combine.R6combine2,
                    3:R6combine.R6combine3}
    loopc = loopclosure.LoopClosure(options.forcefield,
                                    options.keepbound,
                                    options.searchbound)
    loopc.maxsteps = options.maxsteps
    loopc.f_neighbour = neighbour_dict[options.neighbour]
    loopc.f_R6combine = combine_dict[options.combine]
    
    root, ext = os.path.splitext(ifname)
    
    time1 = time.time()
    clock1 = time.clock()
    print time.ctime(time1)
    mol = readxyz(file(ifname))
    goodmol = loopc(ifname)
    counter = 1
    for result in goodmol:
        print '%i: %f, %i' % (counter, result.ene, result.opttimes)
        print '['+', '.join(['%.1f' % tor for tor in statstor(result.mol)])+']'
        writexyz(result.mol, file('%s-%05i%s' % (root, counter, ext), 'w+'))
        counter += 1
    print 'Times of minimize: %i' % tinker.minimize_count
    print time.asctime()
    time2 = time.time()
    clock2 = time.clock()
    print 'Total Time(physical time): %.2fs' % (time2 - time1)
    print resource.getrusage(resource.RUSAGE_SELF)
    print resource.getrusage(resource.RUSAGE_CHILDREN)

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
    parser.add_option('-n', "--neighbour", dest="neighbour",
                      default=1, type='int',
                      help='-n1: Neig I, -n2: Neig II, default: -n1')
    parser.add_option('-c', "--combine", dest="combine",
                      default=3, type='int',
                      help='-c1: Comb I, -c2: Comb II, -c3: Comb III, default: -c3')
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    testcyc(args[0], options)    

if __name__ == '__main__':
    main()
        
