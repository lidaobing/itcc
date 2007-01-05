# $Id$

__revision__ = '$Rev$'

import sys
from itcc.molecule import read
from itcc.tinker import parameter, analyze, tinker, molparam
from itcc.torsionfit import tools, parmfit

def printefit(datfname, idxfname, param):
    '''Only print E_fit'''
    import csv
    fnames, enes, weights = tools.readdat(datfname)
    idxs, folds = parmfit.readidx(idxfname)
    params = parmfit.getparams(idxs, param)
    writer = csv.writer(sys.stdout)
    writer.writerow(['Filename', 'weight', 'E_qm', 'E_mm', 'E_tor', 'E_fit'])
    for fname, E_qm, weight in zip(fnames, enes, weights):
        mol = read.readxyz(file(fname))
        tors = analyze.gettorsbytype(mol, idxs)
        newmol, E_mm = tinker.minimize_file(fname, param)
        E_tor = parmfit.getetor(newmol, tors, params)
        E_fit = E_qm - E_mm + E_tor
        writer.writerow([fname, weight, E_qm, E_mm, E_tor, E_fit])

def main():
    if len(sys.argv) != 4:
        import os.path
        print >> sys.stderr, 'Usage: %s datfname idxfname param' % \
              os.path.basename(sys.argv[0])
        sys.exit(1)
    printefit(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()
