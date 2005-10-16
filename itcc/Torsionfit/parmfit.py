# $Id$

__revision__ = '$Rev$'

import sys
import math
import Numeric
import LinearAlgebra
from itcc.Molecule import read
from itcc.Tinker import parameter, analyze, tinker, molparam
from itcc.Torsionfit import tools

def torene(tor, param):
    """torene(tor, param) -> Float
    tor: Float
    param: List of Float
    """
    result = 0.0

    for i, x in enumerate(param):
        i += 1
        if i % 2 == 1:
            result += 0.5 * x * (1 + math.cos(i * tor))
        else:
            result += 0.5 * x * (1 - math.cos(i * tor))
    return result

def readidx(idxfname):
    idxs = []
    folds = []
    for line in file(idxfname):
        words = line.split()
        if not words:
            continue
        assert 4 <= len(words) <= 5
        idx = tuple([int(x) for x in words[:4]])
        if len(words) == 5:
            fold = int(words[-1])
        else:
            fold = 3
        idxs.append(molparam.torsion_uni(idx))
        folds.append(fold)
    return (idxs, folds)

def getparams(idxs, param):
    result = {}
    for idx in idxs:
        assert len(idx) == 4
        torprm = parameter.readtorsionprm(param, idx[0], idx[1], idx[2], idx[3])
        assert torprm is not None
        result[idx] = torprm
    return result

def getetor(mol, data, params):
    result = 0.0
    for typ, tors in data.items():
        param = params[typ]
        for tor in tors:
            torang = mol.calctor(tor[0], tor[1], tor[2], tor[3])
            result += torene(torang, param)
    return result

def getA(mol, types, folds, data):
    result = [0.0] * (sum(folds) + 1)
    result[-1] = 1.0

    idx = 0

    for typ, fold in zip(types, folds):
        for tor in data[typ]:
            torang = mol.calctor(tor[0], tor[1], tor[2], tor[3])
            for i in range(1, fold+1):
                if i % 2 == 1:
                    result[idx+i-1] += +0.5 * math.cos(i * torang)
                else:
                    result[idx+i-1] += -0.5 * math.cos(i * torang)
        idx += fold
    return result

def printprm(param, types, folds):
    assert len(param) == sum(folds)
    idx = 0
    for typ, fold in zip(types, folds):
        sys.stdout.write(str(parameter.Torsionparameter(list(typ) +
            param[idx:idx+fold])))
        idx += fold

def parmfit(datfname, idxfname, param):
    fnames, enes, weights = tools.readdat(datfname)
    idxs, folds = readidx(idxfname)
    params = getparams(idxs, param)
    A = []
    B = []
    for fname, E_qm, weight in zip(fnames, enes, weights):
        mol = read.readxyz(file(fname))
        tors = analyze.gettorsbytype(mol, idxs)
        newmol, E_mm = tinker.minimize_file(fname, param)
        E_tor = getetor(newmol, tors, params)
        E_fit = E_qm - E_mm + E_tor
        weight = math.sqrt(weight)
        B.append(E_fit * weight)
        A.append([x*weight for x in getA(newmol, idxs, folds, tors)])
    A = Numeric.array(A)
    B = Numeric.array(B)

    result = LinearAlgebra.linear_least_squares(A, B)
    newparam = list(result[0][:-1])
    error = math.sqrt(result[1][0]/len(B))
    printprm(newparam, idxs, folds)
    print error

def printefit():
    '''Only print E_fit'''
    import csv
    if len(sys.argv) != 4:
        import os.path
        print >> sys.stderr, 'Usage: %s datfname idxfname param' % \
              os.path.basename(sys.argv[0])
        sys.exit(1)
    datfname = sys.argv[1]
    idxfname = sys.argv[2]
    param = sys.argv[3]
    fnames, enes, weights = tools.readdat(datfname)
    idxs, folds = readidx(idxfname)
    params = getparams(idxs, param)
    writer = csv.writer(sys.stdout)
    writer.writerow(['Filename', 'weight', 'E_qm', 'E_mm', 'E_tor', 'E_fit'])
    for fname, E_qm, weight in zip(fnames, enes, weights):
        mol = read.readxyz(file(fname))
        tors = analyze.gettorsbytype(mol, idxs)
        newmol, E_mm = tinker.minimize_file(fname, param)
        E_tor = getetor(newmol, tors, params)
        E_fit = E_qm - E_mm + E_tor
        writer.writerow([fname, weight, E_qm, E_mm, E_tor, E_fit])

def main():
    if len(sys.argv) != 4:
        import os.path
        print >> sys.stderr, 'Usage: %s datfname idxfname param' % \
              os.path.basename(sys.argv[0])
        sys.exit(1)
    parmfit(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()
