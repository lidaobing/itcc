# -*- coding: utf-8 -*-
# 
# $Id$
# $Log: molecular.py,v $
# Revision 1.11  2004/08/27 11:32:02  nichloas
# commit at 2004-08-27
#
# Revision 1.10  2004/08/13 12:15:52  nichloas
# * change encoding to utf-8
# * fix a bug in Molecular.copy(connect only need to copy 1 time)
#
# Revision 1.9  2004/02/16 11:21:51  nichloas
# *** empty log message ***
#
# Revision 1.8  2004/02/01 05:17:44  nichloas
# modify molecular.copy()
#
# Revision 1.7  2004/02/01 04:43:31  nichloas
# implement copy
#
# Revision 1.6  2004/02/01 04:05:32  nichloas
# *** empty log message ***
#
# Revision 1.5  2004/02/01 04:04:37  nichloas
# add copy(not implement)
#
# Revision 1.4  2003/12/21 04:33:32  nichloas
# modify: gettypes
# addL cmptopstr
#
# Revision 1.3  2003/12/01 07:57:38  nichloas
# add comment.
#
# 

__version__ = "$Revision: 1.11 $"[11:-2]

import tools
from Numeric import zeros, Float
import pickle
from atom import *

__all__ = ["Molecular"]

        
class Molecular(object):
    __maxbondlen = 1.6

    def __init__(self):
        self.atoms = []
        self.connect = []
        self.distancematrix = None

    def copy(self):
        "return a copy of molecular"
        result = Molecular()
        for x in self.atoms:
            result.atoms.append(x.copy())
        result.connect = pickle.loads(pickle.dumps(self.connect, pickle.HIGHEST_PROTOCOL))
        return result
        
    def __len__(self):
        return len(self.atoms)

    def __getitem__(self, key):
        return self.atoms[key]

    def __setitem__(self, key, value):
        self.atoms[key] = value
        

    def builddistancematrix(self):
        self.distancematrix = zeros((len(self),len(self)), Float)
        
        for i in range(len(self)):
            for j in range(i+1, len(self)):
                distance = tools.distance(self.atoms[i].coords, self.atoms[j].coords)
                self.distancematrix[i,j] = distance
                self.distancematrix[j,i] = distance
                
    # connect system
    def buildconnect(self):
        self.connect = []
        self.builddistancematrix()
        for i in range(len(self)):
            self.connect.append([])
            for j in range(len(self.distancematrix)):
                if j != i and self.distancematrix[i,j] < self.__maxbondlen:
                    self.connect[i].append(j)

    def confirmconnect(self):
        "if connect matrix is not ready, build it"
        if not self.connect:
            self.buildconnect()

    def appendconnect(self, list):
        newlist = [int(x) - 1 for x in list]
        self.connect.append(newlist)

    # types system
    def gettypes(self):
        return [x.type for x in self.atoms]

    def settypes(self, value):
        assert(len(self) == len(value))
        
        for i,x in enumerate(value):
            self.atoms[i].type = x

    types = property(gettypes, settypes)


    def changeorder(self, neworder):
        """
        Attention:
        the neworder format is like
        [5, 4, 6, 3, 2, 1]
        """
        newatoms = []
        for x in neworder:
            newatoms.append(self.atoms[x-1])

        self.atoms = newatoms
        self.connect = []
        self.distacematrix = None

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
        return tools.distance(self.atoms[i-1].coords,
                              self.atoms[j-1].coords)

    def calcang(self, i, j, k):
        "return in radian"
        return tools.angle(self.atoms[i-1].coords,
                           self.atoms[j-1].coords,
                           self.atoms[k-1].coords)

    def calctor(self, i, j, k, l):
        "return in radian"
        return tools.torsionangle(self.atoms[i-1].coords,
                                  self.atoms[j-1].coords,
                                  self.atoms[k-1].coords,
                                  self.atoms[l-1].coords)
    def len(self, i, j):
        return tools.distance(self.atoms[i].coords,
                              self.atoms[j].coords)

    def ang(self, i, j, k):
        "return in radian"
        return tools.angle(self.atoms[i].coords,
                           self.atoms[j].coords,
                           self.atoms[k].coords)

    def tor(self, i, j, k, l):
        "return in radian"
        return tools.torsionangle(self.atoms[i].coords,
                                  self.atoms[j].coords,
                                  self.atoms[k].coords,
                                  self.atoms[l].coords)

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

    def cmptopstr(self, other):
        '''比较拓朴结构
        过时的，建议使用 cmpmol.cmptopstr
        '''
        if len(self.atoms) != len(other.atoms):
            return False
        for i in xrange(len(self.atoms)):
            if self.atoms[i]._no != other.atoms[i]._no:
                return False
        self.confirmconnect()
        other.confirmconnect()

        if self.connect != other.connect:
            return False
        else:
            return True
