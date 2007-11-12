# $Id$

__revision__ = '$Rev$'

import math
import sys

from itcc.core import IgnoreEpipe
from itcc.molecule import mtxyz

def readidx(ifile):
    result = []
    for line in ifile:
        words = line.split()
        if len(words) == 0:
            continue
        assert len(words) in (2, 3, 4)
        result.append(tuple([int(word) - 1 for word in words]))
    return result

def print_idx(idxs, ofile):
    ofile.write('Name ')
    ofile.write('\t'.join(['-'.join([str(x+1) for x in idx]) for idx in idxs]) + '\n')

def mol_calc_wrap(mol, idx):
    if len(idx) == 2:
        return mol.calclen(idx[0], idx[1])
    elif len(idx) == 3:
        return math.degrees(mol.calcang(idx[0], idx[1], idx[2]))
    elif len(idx) == 4:
        return math.degrees(mol.calctor(idx[0], idx[1], idx[2], idx[3]))
    else:
        assert False

def molstat(mol, idxs, ofile):
    result = [mol_calc_wrap(mol, idx) for idx in idxs]
    ofile.write('\t'.join([str(x) for x in result]) + '\n')
    ofile.flush()

def mtxyzstat(mtxyzfname, idxs, ofile):
    for mol in mtxyz.Mtxyz(file(mtxyzfname)):
        molstat(mol, idxs, ofile)

def main():
    from optparse import OptionParser

    usage = 'usage: %prog [-H|--header] [-v] -I idx-file mtxyzfname...'
    parser = OptionParser(usage)
    parser.add_option('-H', '--header',
                      action='store_true', dest='print_header',
                      help='print header')
    parser.add_option('-v', '--verbose',
            action = 'store_true',
            dest = 'verbose',
            help = 'print filename')
    parser.add_option('-I', '--idx-file',
                      dest='idx_file',
                      metavar='FILE',
                      help='index file, "-" means stdin, index is 1-based')
    (options, args) = parser.parse_args()

    if len(args) < 1 or options.idx_file is None:
        parser.error("incorrect number of arguments")

    if options.idx_file == '-':
        idx_ifile = sys.stdin
    else:
        idx_ifile = file(options.idx_file)

    idxs = readidx(idx_ifile)

    ofile = IgnoreEpipe(sys.stdout)
    if options.print_header:
        print_idx(idxs, ofile)

    for arg in args:
        if options.verbose:
            ofile.write('%s ' % arg)
        mtxyzstat(arg, idxs, ofile)

if __name__ == '__main__':
    main()
