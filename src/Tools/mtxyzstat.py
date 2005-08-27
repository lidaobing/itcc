# $Id$

__revision__ = '$Rev$'

import math
from itcc.Molecule import mtxyz

def readidx(ifile):
    result = []
    for line in ifile:
        words = line.split()
        if len(words) == 0:
            continue
        assert len(words) in (2, 3, 4)
        result.append(tuple([int(word) - 1 for word in words]))
    return result

def print_idx(idxs):
    print '\t'.join(['-'.join([str(x+1) for x in idx]) for idx in idxs])

def mol_calc_wrap(mol, idx):
    if len(idx) == 2:
        return mol.calclen(idx[0], idx[1])
    elif len(idx) == 3:
        return math.degrees(mol.calcang(idx[0], idx[1], idx[2]))
    elif len(idx) == 4:
        return math.degrees(mol.calctor(idx[0], idx[1], idx[2], idx[3]))
    else:
        assert False

def molstat(mol, idxs):
    result = [mol_calc_wrap(mol, idx) for idx in idxs]
    print '\t'.join([str(x) for x in result])

def mtxyzstat(mtxyzfname, idxs, print_header=False):
    if(print_header):
        print_idx(idxs)
    for mol in mtxyz.Mtxyz(file(mtxyzfname)):
        molstat(mol, idxs)

def main():
    import sys
    from optparse import OptionParser

    usage = 'usage: %prog [-H|--header] mtxyzfname {-|idxfname}'
    parser = OptionParser(usage)
    parser.add_option('-H', '--header',
                      action='store_true', dest='print_header',
                      help='print header')
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("incorrect number of arguments")

    if args[1] == '-':
        idx_ifile = sys.stdin
    else:
        idx_ifile = file(args[1])

    idxs = readidx(idx_ifile)

    mtxyzstat(args[0], idxs, options.print_header)

if __name__ == '__main__':
    main()
