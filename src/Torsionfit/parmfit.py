#!/usr/bin/env python
# -*- coding: gb2312 -*-

__revision__ = '$Id$'

import Numeric
import math
import LinearAlgebra

__DEBUG__ = 1

def torene(tors, param):
    """torene(tors, param) -> Array of Float
    tors: List/Array of Float
    param: List of Float
    """

    tors = Numeric.array(tors)

    result = Numeric.zeros(len(tors), 'd')

    for i,x in enumerate(param):
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
    for x,y in params.iteritems():
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


def main():
    pass

if __name__ == '__main__':
    main()
