# $Id$
import itcc
from itcc.ccs2 import loopclosure

__revision__ = '$Rev$'

def testcyc(ifname, options):
    if options.resume is not None:
        import cPickle
        loopc = cPickle.load(file(options.resume))
        loopc(ifname)
        return

    loopc = loopclosure.LoopClosure()
    loopc.forcefield = options.forcefield
    loopc.keeprange = options.keepbound
    loopc.searchrange = options.searchbound
    loopc.maxsteps = options.maxsteps
    loopc.moltypekey = options.moltype
    loopc.dump_steps = options.dump_interaval

    if options.loop is None and options.loopfile is not None:
        options.loop = file(options.loopfile).read()
    if options.loop is not None:
        loopc.loop = [int(x)-1 for x in options.loop.split()]

    if options.chiral_index_file is not None and options.chiral_index is None:
        options.chiral_index = file(options.chiral_index_file).read()
    if options.chiral_index is not None:
        loopc.check_chiral = True
        loopc.chiral_idxs = [int(x)-1 for x in options.chiral_index.split()]
        
    if options.legal_min_ene is not None:
        loopc.legal_min_ene = options.legal_min_ene
    loopc(ifname)

def main():
    from optparse import OptionParser

    usage = "usage: %prog [-h|options] xyzfile\n" \
            "       %prog --resume checkfile"
    parser = OptionParser(usage,
                          version = itcc.__version__
                          )
    parser.set_defaults(dump_interaval=100)
    parser.add_option("-f", "--forcefield", dest='forcefield',
                      default='mm2', help="default is mm2")
    parser.add_option('-k', "--keep", dest="keepbound",
                      default=None, type='float',
                      help='keep boundary(kcal/mol), default is no boundary')
    parser.add_option('-s', "--search", dest="searchbound",
                      default=None, type='float',
                      help='search boundary(kcal/mol), default is no boundary')
    parser.add_option('-m', "--maxsteps", dest="maxsteps",
                      default=None, type='int',
                      help='max optimization steps, default is '
                           'infinite')
    parser.add_option('-t', "--moltype", dest="moltype",
                      default=None, help='you can set it to peptide')
    parser.add_option('-l', '--legal-min-ene', dest='legal_min_ene',
                      default=None, help='in some forcefield (e.g. OPLSAA), '
                      'there some illegal structure with extremely '
                      'low energy (e.g. -13960945.7658 kcal/mol), so '
                      'we treat all structure with energy lower than '
                      'LEGAL_MIN_ENE is illegal, default is %f kcal/mol'
                      % loopclosure.LoopClosure.legal_min_ene)
    parser.add_option('--loop', dest='loop',
                      default=None, help='specify loop instead of auto-detect, begin with 1')
    parser.add_option('--loopfile', 
                      dest='loopfile',
                      default=None,
                      metavar='FILE',
                      help='specify loop instead of auto-detect, '
                           'this option will be ignored if used with --loop.')
    parser.add_option('--chiral-index',
                      dest='chiral_index',
                      default=None,
                      help='keep chiral and provide chiral indexes, begin with 1')
    parser.add_option('--chiral-index-file',
                      dest='chiral_index_file',
                      default=None,
                      metavar='FILE',
                      help='similar with --chiral-index, read from a file, ignored if used with --chiral-index')
    parser.add_option('--resume',
                      dest='resume',
                      default=None,
                      metavar='FILE',
                      help='resume')
    parser.add_option('--dump-interval',
                      dest='dump_interaval',
                      type='int',
                      metavar='INT',
                      help='dump interval, default is 100 steps')

    (options, args) = parser.parse_args()
    if options.resume is None:
        if len(args) != 1:
            parser.error("incorrect number of arguments")
        testcyc(args[0], options)
    else:
        if len(args) != 0:
            parser.error("incorrect number of arguments")
        testcyc(None, options)

if __name__ == '__main__':
    main()

