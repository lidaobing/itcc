# $Id$
import Numeric

__revision__ = '$Rev$'

def distmat(mol):
    size = len(mol)
    result = Numeric.zeros((size, size), Numeric.Float)

    for i in range(size):
        for j in range(i):
            distance = (mol.coords[i] - mol.coords[j]).length()
            result[i, j] = distance
            result[j, i] = distance
    return result
