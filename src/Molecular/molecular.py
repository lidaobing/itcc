# -*- coding: utf-8 -*-

import pprint
from Numeric import zeros, Float, Int
from Scientific.Geometry import Vector
from itcc.Tools import tools
from atom import *

__all__ = ["Molecular"]
        
class Molecular(object):
    __maxbondlen = 1.6

    def __init__(self, atoms = None, coords = None, connect = None):
        self.atoms = atoms or []
        self.coords = coords or []
        self.connect = connect

    def __getstate__(self):
        return [self.atoms, self.coords, self.connect]

    def __setstate__(self, state):
        self.atoms = state[0]
        self.coords = state[1]
        self.connect = state[2]

    def __copy__(self):
        return Molecular(self.atoms[:], self.coords[:], self.connect)

    __deepcopy__ = __copy__

    def __len__(self):
        return len(self.atoms)

    def __getitem__(self, key):
        return (self.atoms[key], self.coords[key])

    def __setitem__(self, key, value):
        self.atoms[key], self.coords[key] = value

    def __str__(self):
        results = ['Molecular(\n']
        results.append(pprint.pformat(self.atoms))
        results.append(',\n')
        results.append(pprint.pformat(self.coords))
        results.append(',\n')
        results.append(`self.connect`)
        results.append(')')
        return ''.join(results)

    __repr__ = __str__

    def __cmp__(self, other):
        return 0
        
    def addatom(self, atom, coord, pos = None):
        if pos is None:
            pos = len(self)
        self.atoms.insert(pos, atom)
        self.coords.insert(pos, coord)
        self.connect = None

    def builddistancematrix(self):
        self.distancematrix = zeros((len(self),len(self)), Float)
        
        for i in range(len(self)):
            for j in range(i):
                distance = tools.distance(self.atoms[i].coords, self.atoms[j].coords)
                self.distancematrix[i,j] = distance
                self.distancematrix[j,i] = distance
                
    # connect system
    def makeconnect(self):
        self.builddistancematrix()
        self.connect = self.distancematrix < self.__maxbondlen

    def buildconnect(self, i, j):
        if not self.connect:
            self.connect = zeros((len(self), len(self)))
        self.connect[i,j] = self.connect[j,i] = 1

    def delconnect(self, j, i):
        self.connect[i,j] = self.connect[j,i] = 0

    def mainchain(self):
        """
        return a new Molecular object, 去掉所有的H原子
        """
        result = Molecular()
        for x in self.atoms:
            if x.no != 1:                # 如果x不是H原子
                result.atoms.append(x.copy())
        return result

    def calclen(self, i, j):
        coords = self.coords
        return (coords[i] - coords[j]).length()

    def calcang(self, i, j, k):
        "return in radian"
        coords = self.coords
        return (coords[k] - coords[j]).angle(coords[i]-coords[j])

    def calctor(self, i, j, k, l):
        "return in radian"
        coords = self.coords
        return tools.torsionangle(coords[i],
                                  coords[j],
                                  coords[k],
                                  coords[l])

    def center(self):
        '''
        return the mass center of the molecular (x0, y0, z0)
        if there is no atom, return (0.0, 0.0, 0.0)
        '''
        if len(self) == 0:
            return (0.0, 0.0, 0.0)

        result = [0.0, 0.0, 0.0]
        molweight = 0.0
        for atom in self.atoms:
            molweight += atom.mass
            result[0] += atom.mass * atom.x
            result[1] += atom.mass * atom.y
            result[2] += atom.mass * atom.z

        result = tuple([x/molweight for x in result])
        return result

    def reorder(self, neworder):
        '''build a new Molecular with neworder, keep connect, you can only
        keep a subset of old atoms'''
        class IdxAtom:
            def __init__(self, atom, coord, idx):
                self.atom = atom
                self.coord = coord
                self.idx = idx
        atoms = []
        connects = []
        for i in range(len(self)):
            atoms.append(IdxAtom(self.atoms[i], self.coords[i], i))
        for i in range(len(self)):
            for j in range(i):
                if self.connect[i,j]:
                    connects.append((atoms[i], atoms[j]))

        newatoms = []
        for newidx, oldidx in enumerate(neworder):
            atoms[oldidx].idx = newidx
            newatoms.append(atoms[oldidx])
        
        result = Molecular()
        for idxatom in newatoms:
            result.addatom(idxatom.atom, idxatom.coord)
        for connect in connects:
            if connect[0] in newatoms and connect[1] in newatoms:
                result.buildconnect(connect[0].idx, connect[1].idx)
        return result

    def settype(self, idx, newtype):
        oldatom = self.atoms[idx]
        newatom = Atom(oldatom.no, newtype, oldatom.symbol)
        self.atoms[idx] = newatom
