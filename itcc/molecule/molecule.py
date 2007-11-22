# $Id$
# -*- coding: utf-8 -*-

import pprint
import math
import numpy
from itcc.core import tools
from itcc.molecule.atom import Atom
from itcc.molecule import tools as moltools

__all__ = ["Molecule", 'CoordType']
__revision__ = '$Rev$'

CoordType = numpy.array

class Molecule(object):
    __maxbondlen = 1.6
    __maxbondlen_h = 1.3

    def __init__(self, atoms = None, coords = None, connect = None):
        if atoms is None:
            self._atoms = []
        else:
            self._atoms = atoms[:]
            
        if coords is not None:
            self._coords = numpy.array(coords)
        else:
            self._coords = numpy.zeros((0, 3), float)
        assert len(self.coords.shape) == 2, \
            (coords, self.coords, self.coords.shape)
        assert self.coords.shape[1] == 3, self.coords
        assert len(self.atoms) == len(self.coords)

        if connect is None:
            self._connect = None
        else:
            self._connect = numpy.array(connect)
            assert self.connect.shape == (len(atoms), len(atoms)), self.connect.shape

    def get_atoms(self):
        return self._atoms
    atoms = property(get_atoms)

    def get_coords(self):
        res = self._coords.view()
        res.setflags(write=False)
        return res
    def set_coords(self, val):
        if val.shape != (len(self), 3):
            raise ValueError("wrong array shape: %s" % val.shape)
        if isinstance(val, numpy.ndarray):
            self._coords = val.copy()
        else:
            self._coords = numpy.array(val)
    coords = property(get_coords, set_coords)

    def change_coord(self, idx, coord):
        self._coords[idx] = coord

    def get_connect(self):
        return self._connect
    connect = property(get_connect)

    def __copy__(self):
        return Molecule(self.atoms, self.coords, self.connect)

    __deepcopy__ = __copy__
    copy = __copy__

    def __len__(self):
        return len(self.atoms)

    def __getitem__(self, key):
        return (self.atoms[key], self.coords[key])

    def __setitem__(self, key, value):
        self.atoms[key], self.coords[key] = value

    def __str__(self):
        results = ['Molecule(\n']
        results.append(pprint.pformat(self.atoms))
        results.append(',\n')
        results.append(pprint.pformat(self.coords))
        results.append(',\n')
        results.append(`self.connect`)
        results.append(')')
        return ''.join(results)

    __repr__ = __str__

    def addatom(self, atom, coord, pos = None):
        if pos is None:
            pos = len(self)
        self.atoms.insert(pos, atom)
        self._coords = numpy.resize(self.coords, (len(self.atoms), 3))
        self._coords[pos+1:,:] = self.coords[pos:-1,:]
        self._coords[pos] = numpy.array(coord)
        self._connect = None

    # connect system
    def is_connect(self, i, j):
        return bool(self.connect[i,j])

    def makeconnect(self):
        distmat = moltools.distmat(self)
        self._connect = numpy.zeros((len(self), len(self)),
                                   bool)
        for i in range(len(self)):
            for j in range(i):
                if self.atoms[i].no == 1 or self.atoms[j].no == 1:
                    self.connect[i][j] = self.connect[j][i] = distmat[i][j] < self.__maxbondlen_h
                else:
                    self.connect[i][j] = self.connect[j][i] = distmat[i][j] < self.__maxbondlen

    def confirmconnect(self):
        if self.connect is None:
            self.makeconnect()

    def buildconnect(self, i, j):
        if self.connect is None:
            self._connect = numpy.zeros((len(self), len(self)), int)
        self.connect[i, j] = self.connect[j, i] = 1

    def delconnect(self, j, i):
        self.connect[i, j] = self.connect[j, i] = 0

    def mainchain(self):
        """
        return a new Molecule object, 去掉所有的H原子
        """
        result = Molecule()
        for x in self.atoms:
            if x.no != 1:                # 如果x不是H原子
                result.atoms.append(x.copy())
        return result

    def calclen(self, i, j):
        coords = self.coords
        t = coords[i] - coords[j]
        return math.sqrt(sum(t*t))

    def calcang(self, i, j, k):
        "return in radian"
        coords = self.coords
        t1 = coords[k] - coords[j]
        t2 = coords[i] - coords[j]
        cos_ = sum(t1*t2)/math.sqrt(sum(t1*t1) * sum(t2*t2))
        return math.acos(max(min(cos_, 1), -1))

    def calctor(self, i, j, k, l):
        "return in radian"
        coords = self.coords
        return tools.torsionangle(coords[i],
                                  coords[j],
                                  coords[k],
                                  coords[l])

    def center(self):
        '''
        return the mass center of the Molecule (x0, y0, z0)
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
        '''build a new Molecule with neworder, keep connect, you can only
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
                if self.connect[i, j]:
                    connects.append((atoms[i], atoms[j]))

        newatoms = []
        for newidx, oldidx in enumerate(neworder):
            atoms[oldidx].idx = newidx
            newatoms.append(atoms[oldidx])

        result = Molecule()
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
