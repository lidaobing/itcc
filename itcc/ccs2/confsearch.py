# $Id$
import itcc
from itcc.ccs2 import loopclosure

try:
    import psyco
    psyco.full()
except ImportError: #pylint: disable-msg=W0704
    pass 

__revision__ = '$Rev$'

def run(ifname, options):
    if options.resume is not None:
        import cPickle
        loopc = cPickle.load(file(options.resume))
        loopc(ifname)
        return

    config = loopclosure.LoopClosure.get_default_config()

    if options.config is not None:
        config.read(options.config)    
    del options.config

    for key, val in options.__dict__.items():
        if val is not None:
            for k, v in loopclosure.LoopClosure.config_keys.items():
                if key in [x[0] for x in v]:
                    sect = k
                    break
            config.set(sect, key, str(val))
    
    config.set('DEFAULT', 'molfname', ifname)

    loopc = loopclosure.LoopClosure(config)
    loopc.run()

def main():
    from optparse import OptionParser
    config = loopclosure.LoopClosure.get_default_config()

    usage = "usage: %prog [options] xyzfile|-\n" \
            "       %prog --resume checkfile\n" \
            "       %prog -h"
    parser = OptionParser(
        usage,
        version = itcc.__version__)
    parser.add_option(
        "--config",
        dest='config',
        metavar='FILE',
        help="load config file")
    parser.add_option(
        "-f",
        "--forcefield",
        dest='forcefield',
        help="default is mm2")
    parser.add_option(
        '-k',
        "--keep",
        dest="keeprange",
        type='float',
        help='keep boundary(kcal/mol), default is no boundary')
    parser.add_option(
        '-s',
        "--search",
        dest="searchrange",
        type='float',
        help='search boundary(kcal/mol), default is no boundary')
    parser.add_option(
        '-m',
        "--maxsteps",
        dest="maxsteps",
        type='int',
        help='max optimization steps, default is infinite')
    parser.add_option(
        '-t',
        "--moltype",
        dest="moltypekey",
        help="you can set it to `peptide'")
    parser.add_option(
        '-l',
        '--legal-min-ene',
        dest='legal_min_ene',
        help='in some forcefield (e.g. OPLSAA), ' \
            'there some illegal structure with extremely ' \
            'low energy (e.g. -13960945.7658 kcal/mol), so ' \
            'we treat all structure with energy lower than ' \
            'LEGAL_MIN_ENE is illegal, default is %.1f kcal/mol' \
            % config.getfloat('DEFAULT', 'legal_min_ene'))
    parser.add_option(
        '--loopfile', 
        dest='loopfile',
        metavar='FILE',
        help='specify loop instead of auto-detect, begin with 1')
    parser.add_option(
        '--chain',
        dest='is_chain',
        action='store_true',
        help="it is a CHAIN, not a loop")
    parser.add_option(
        '--cmptors',
        dest='cmptorsfile',
        metavar='FILE',
        help='a file contains all torsion angle used to identify a molecule, '
             'each line in this file have 4 columns, echo column is the '
             'atom\'s index, 1-based, by default, these tors are generated '
             'from the loop information and chain information')
    parser.add_option(
        '--achiral',
        dest='is_achiral',
        action='store_true',
        help='tors -> [-x for x in tors]')
    parser.add_option(
        '--chiral',
        dest='is_achiral',
        action='store_false',
        help='disable --achiral')
    parser.add_option(
        '--head-tail',
        dest='head_tail',
        type='int',
        metavar='INT',
        help='tors -> (tos[i:] + tors[:i])[::-1]')
    parser.add_option(
        '--loop-step',
        dest='loopstep',
        type='int',
        metavar='INT',
        help='tors -> tos[i:] + tors[:i]')
   
    parser.add_option(
        '--chiral-index',
        dest='chiral_index',
        help='keep chiral and provide chiral indexes, begin with 1')
    parser.add_option(
        '--chiral-index-file',
        dest='chiral_index_file',
        default=None,
        metavar='FILE',
        help='similar with --chiral-index, read from a file, ignored if ' \
            'used with --chiral-index')
    parser.add_option(
        '--resume',
        dest='resume',
        metavar='FILE',
        help='resume')
    parser.add_option(
        '--dump-interval',
        dest='dump_steps',
        type='int',
        metavar='INT',
        help='dump interval, default is 100 steps')
    parser.add_option(
        '--np',
        dest='np',
        type='int',
        metavar='INT',
        help='number of processor, default is 1')
    parser.add_option(
        '--solvate',
        dest='solvate',
        type='choice',
        choices=('asp', 'sasa', 'onion', 'still',
                 'hct', 'ace', 'gbsa'),
        metavar='NAME',
        help='set solvate model')
    parser.add_option(
        '-c', '--check-energy-before-minimization',
        dest='check_energy_before_minimization',
        action='store_true',
        help='check energy before minimization' \
            + ('', ', this is the default') \
            [config.getboolean('DEFAULT', 'check_energy_before_minimization')])
    parser.add_option(
        '-C',
        '--no-check-energy-before-minimization',
        dest='check_energy_before_minimization',
        action='store_false',
        help="don't check energy before minimization" \
            + (', this is the default', '') \
            [config.getboolean('DEFAULT', 'check_energy_before_minimization')])
    parser.add_option(
        '-e',
        '--minimal-invalid-energy-before-minimization',
        dest='minimal_invalid_energy_before_minimization',
        type='float',
        metavar='ENE',
        help="minimal invalid energy before minimization, " \
            "unit is kcal/mol, default is %.1f" \
            % config.getfloat('DEFAULT', 'minimal_invalid_energy_before_minimization'))
    parser.add_option(
            '--log-iter',
            dest='log_iter',
            action='store_true')
                      
    (options, args) = parser.parse_args()
    if options.resume is None:
        if len(args) != 1:
            parser.error("incorrect number of arguments")
        run(args[0], options)
    else:
        if len(args) != 0:
            parser.error("incorrect number of arguments")
        run(None, options)

if __name__ == '__main__':
    main()

