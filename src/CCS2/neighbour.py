# $Id$
import math
import random
import sys
from itcc.Molecule.molecule import Molecule
from itcc.Tools.tools import combinecombine, torsionangle
from itcc.Tinker import tinker
from itcc.CCS2 import shakeH, getshakeHdata, loopdetect
from itcc.CCS2.tors import TorsSet
from itcc.CCS2.R6combine import R6combine1
from itcc.CCS2 import R6

__all__ = ['calctor', 'Neighbour', 'NeighbourI', 'NeighbourII']

def calctor(coords, loopatoms):
    'return in degrees'
    doubleloop = loopatoms * 2
    return tuple([math.degrees
                  (torsionangle(*tuple([coords[j] for j in doubleloop[i:i+4]])))
                  for i in range(len(loopatoms))])

class NeighbourConfig:
    def __init__(self, mol, forcefield):
        self.mol = mol
        self.forcefield = forcefield
        self.loopatoms = self.getloopatoms(mol)
        self.R6s = self.getR6s(self.loopatoms)
        self.combinations = self.getcombinations(self.R6s)
        tors = calctor(mol.coords, self.loopatoms)
        self.knowntors = TorsSet([tors])
        self.knownmols = TorsSet([tors])
        self.shakeHdata = getshakeHdata(mol)
        
    def getloopatoms(self, mol):
        loops = loopdetect(mol)
        assert len(loops) == 1
        return loops[0]
        
    def getR6s(loopatoms):
        doubleloop = loopatoms * 2
        return [tuple(doubleloop[i:i+7]) for i in range(len(loopatoms))]
    getR6s = staticmethod(getR6s)

    def getcombinations(R6s):
        size = len(R6s)
        return R6combine1(R6s)
    getcombinations = staticmethod(getcombinations)
        

class Neighbour:
    def __init__(self, mol, ene, lc):
        self.mol = mol
        self.ene = ene
        self.coords = mol.coords
        self.loopatoms = lc.loopatoms
        self.R6s = lc.R6s
        self.combinations = lc.combinations
        self.knownmols = lc.knownmols
        self.forcefield = lc.forcefield
        self.shakeHdata = lc.shakeHdata
        self.lc = lc
        
    def init(self):

        self.R6results = {}
        for R6idx in self.R6s:
            self.R6results[R6idx] = R6.R6_in_vivo(
                [self.coords[idx] for idx in R6idx])

        self.coordsset = []
        coords = self.coords
        for combine in self.combinations:
            R6s = [self.R6results[x] for x in combine]
            result = list(combinecombine(R6s))
	    for x in result:
                newcoords = coords[:]
                for atmidxs, _coords in zip(combine, x):
                    newcoords[atmidxs[2]] = _coords[2]
                    newcoords[atmidxs[3]] = _coords[3]
                    newcoords[atmidxs[4]] = _coords[4]
                self.coordsset.append(tuple(newcoords))
        random.shuffle(self.coordsset)
        self.totaltask = len(self.coordsset)

    def __iter__(self):
        return self
        
    def next(self):
        self.init()
        self.next = self._next
        return self._next()
    
    def _next(self):
        if not self.coordsset:
            raise StopIteration
        newcoords = list(self.coordsset.pop())

        shakeH(newcoords, self.shakeHdata)
        newmol = Molecule(self.mol.atoms, newcoords, self.mol.connect)
        newmol, ene = tinker.minimizemol(newmol, self.forcefield, 0.001)
        tors = calctor(newmol.coords, self.loopatoms)

        if tors in self.knownmols:
            return None, None
        
        self.knownmols.append(tors)
        return newmol, ene
            
    def gettotaltask(self):
        if not self.inited():
            return None
        return self.totaltask
    def finishedtask(self):
        if not self.inited():
            return None
        return self.totaltask - len(self.coordsset)

    def getprogress(self):
        if not self.inited():
            return 0.0
        return 1.0 - float(len(self.coordsset))/self.totaltask

    def inited(self):
        return self.next == self._next
                    
class NeighbourI(Neighbour):
    idstr = 'Neig I'
    def __cmp__(self, other):
        return cmp(self.ene, other)
    
class NeighbourII(Neighbour):
    idstr = 'Neig II'
    def __cmp__(self, other):
        return cmp((self.finishedtask,self.ene), other)
    
    
