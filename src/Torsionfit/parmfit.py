# -*- coding: gb2312 -*-
# $Id$

__revision__ = '$Rev$'

import math
import Numeric
import LinearAlgebra
from itcc.Molecule import read
from itcc.Tinker import parameter, analyze

__DEBUG__ = 1

def torene(tors, param):
    """torene(tors, param) -> Array of Float
    tors: List/Array of Float
    param: List of Float
    """

    tors = Numeric.array(tors)

    result = Numeric.zeros(len(tors), 'd')

    for i, x in enumerate(param):
        i += 1
        if i % 2 == 1:
            result += 0.5 * x * (1 + Numeric.cos(i * tors))
        else:
            result += 0.5 * x * (1 - Numeric.cos(i * tors))
    return result
    
def genparam(types, param):
    """genparam(types, param) -> String
    """
    fmtstr = 'torsion   %4i %4i %4i %4i  '
    for i in range(1, len(param)+1):
        if i % 2 == 1:
            fmtstr = fmtstr + ' %8.3f 0.0 ' + '%d' % i
        else:
            fmtstr = fmtstr + ' %8.3f 180.0 ' + '%d' % i
    fmtstr += '\n'
    
    return fmtstr % tuple(list(types) + list(param))

def genparams(params):
    """genparams(params) -> List of String
    params: Mappings
    """
    results = []
    for x, y in params.iteritems():
        results.append(genparam(x, y))
    return results


def fitparam(thetas, E_fit, fold = 3):
    """fitparam(thetas, E_fit, fold = 3) -> (newparam, error)
    thetas: List of Float
    E_fit: List of Float
    fold: integer
    
    newparam: List of Float
    error: Float, the RMS error
    """

    thetas = Numeric.array(thetas)
    E_fit = Numeric.array(E_fit)
    A = []

    for i in range(1, fold+1):
        if i % 2 == 1:
            A.append(+0.5 * Numeric.cos(i * thetas))
        else:
            A.append(-0.5 * Numeric.cos(i * thetas))
        

    A.append(Numeric.array([1.0] * len(thetas)))
    
    A = Numeric.swapaxes(Numeric.array(A), 0, 1)
    B = E_fit
    
    result = LinearAlgebra.linear_least_squares(A, B)
    newparam = result[0][:-1]
    error = math.sqrt(result[1][0]/len(E_fit))

    return newparam, error

def readdat(datfname):
    fnames = []
    enes = []
    weights = []
    for line in file(datfname):
        fname, ene, weight = tuple(line.split())
        fnames.append(fname)
        enes.append(float(ene))
        weights.append(weight)
    return (fnames, enes, weights)

def readidx(idxfname):
    idxs = []
    folds = []
    for line in file(idxfname):
        words = line.split()
        assert 4 <= len(words) <= 5
        idx = tuple([int(x) for x in words[:4]])
        if len(words) == 5:
            fold = int(words[-1])
        else:
            fold = 3
        idxs.append(idx)
        folds.append(fold)
    return (idxs, folds)

def getparams(idxs, param):
    result = []
    for idx in idxs:
        assert len(idx) == 4
        torprm = parameter.readtorsionprm(param, idx[0], idx[1], idx[2], idx[3])
        assert torprm is not None
        result.append(torprm)
    return result
        

def parmfit(datfname, idxfname, param):
    fnames, enes, weights = readdat(datfname)
    idxs, folds = readidx(idxfname)
    params = getparams(idxs, param)
    for fname in datfname:
        mol = read.readxyz(file(fname))
        print analyze.gettorsbytype(mol, idxs)
        return

def main():
    pass

if __name__ == '__main__':
    main()
