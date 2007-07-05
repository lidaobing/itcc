# $Id$

import sys
import csv
from itcc.molecule import read, rmsd
from itcc.core import tools
from itcc.torsionfit import tools as tortools
from itcc.tinker import tinker

__revision__ = '$Rev$'


def parmeval(datfname, param):
    fnames, enes, weights = tortools.readdat(datfname)
    writer = csv.writer(sys.stdout)
    writer.writerow(['Filename', 'weight', 'E_qm', 'E_mm', 'E_diff', 'RMSD'])
    E_diffs = []
    rmsds = []
    for fname, E_qm, weight in zip(fnames, enes, weights):
        mol = read.readxyz(file(fname))
        newmol, E_mm = tinker.minimize_file(fname, param)
        E_diff = E_mm - E_qm
        E_diffs.append(E_diff)
        rmsd_ = rmsd.rmsd(mol, newmol)
        rmsds.append(rmsd_)
        row = [fname, weight, E_qm, E_mm, E_diff, rmsd_]
        writer.writerow(row)
    writer.writerow([])
    writer.writerow(['Weighted Averrage of E_diff',
                     tools.weightedmean(E_diffs, weights)])
    writer.writerow(['Weighted SD of E_diff',
                     tools.weightedsd(E_diffs, weights)])
    writer.writerow(['Weighted Average of RMSD',
                     tools.weightedmean(rmsds, weights)])

def main():
    if len(sys.argv) != 3:
        import os.path
        print >> sys.stderr, 'Usage: %s datfname param' % \
              os.path.basename(sys.argv[0])
        sys.exit(1)
    parmeval(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()

