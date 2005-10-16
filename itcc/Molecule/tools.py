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

def gettypes(mol):
    return [atom.type for atom in mol.atoms]

def calclooptor(mol, loop):
    doubleloop = loop * 2
    tors = [mol.calctor(*doubleloop[i:i+4]) for i in range(len(loop))]
    return tors

def connectatoms(mol, atmidx):
    connect = mol.connect[atmidx]
    return [idx for idx, data in enumerate(connect)
            if data]

def neighborlist(mol):
    '''return the neighborlist
    for example, for CH4, will return
    [[1, 2, 3, 4],
    [0],
    [0],
    [0],
    [0]]
    '''
    result = []
    for atmidx in range(len(mol.atoms)):
        result.append(connectatoms(mol, atmidx))
    return result

