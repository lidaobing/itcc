# -*- coding: utf8 -*-
# $Id$

from itcc.Molecule import read, relalist
from itcc.Tools import tools

__revision__ = '$Rev$'

class Cmpresabs:
    "Abstract Compare Result Class"
    def __init__(self, *args):
        if len(args) == 1:
            self._cmpres = args[0]
        else:
            self._cmpres = args

    def __cmp__(self, other):
        if isinstance(other, Cmpresabs):
            return cmp(abs(self._cmpres[3]), abs(other._cmpres[3]))
        else:
            return cmp(abs(self._cmpres[3]), other)

    def _str(self, config):
        result = "%s: " + config * 3
        return result % tuple(self._cmpres)

    def __getitem__(self, index):
        return self._cmpres[index]

class Cmpresbon(Cmpresabs):
    def __str__(self):
        return self._str("%9.5f")

class Cmpresang(Cmpresabs):
    def __str__(self):
        return self._str("%8.2f")

class Cmprestor(Cmpresabs):
    def __str__(self):
        return self._str("%8.2f")

class Cmpresult:
    def __init__(self):
        self.bonds = []
        self.angles = []
        self.torsions = []
        self.displacement = []


    def maxbondchange(self):
        return max(self.bonds)

    def maxanglechange(self):
        return max(self.angles)

    def maxtorsionchange(self):
        return max(self.torsions)

    def disRMS(self):
        return tools.RMS([x[1] for x in self.displacement])

    def __str__(self):
        result = []
        result.append('Bonds: %i\n' % len(self.bonds))
        for x in self.bonds:
            result.append(str(x)+'\n')

        result.append('\nAngles: %i\n' % len(self.angles))
        for x in self.angles:
            result.append(str(x)+'\n')

        result.append('\nTorsions: %i\n' % len(self.torsions))
        for x in self.torsions:
            result.append(str(x)+'\n')

        return ''.join(result)

class Batchcmpresult(list):
    def disRMS(self):
        data = []
        for cmpres in self:
            data.extend([x[1] for x in cmpres.displacement])
        return tools.RMS(data)
    def dismean(self):
        data = []
        for cmpres in self:
            data.extend([x[1] for x in cmpres.displacement])
        return tools.mean(data)
    def dismax(self):
        data = []
        for cmpres in self:
            data.extend([x[1] for x in cmpres.displacement])
        return max(data)

def cmpmol(mol1, mol2, cmplist = None):
    if cmplist is None:
        cmplist1 = relalist.Relalist(mol1)
        cmplist2 = relalist.Relalist(mol2)
        if cmplist1 == cmplist2:
            cmplist = cmplist1
        else:
            raise ValueError

    result = Cmpresult()

    for x in cmplist.bonds:
        b1 = mol1.calclen(x[0], x[1])
        b2 = mol2.calclen(x[0], x[1])
        result.bonds.append(Cmpresbon(x, b1, b2, b1-b2))

    for x in cmplist.angles:
        b1 = mol1.calcang(x[0], x[1], x[2])
        b2 = mol2.calcang(x[0], x[1], x[2])
        result.angles.append(Cmpresang(x, b1, b2, b1-b2))

    for x in cmplist.torsions:
        b1 = mol1.calctor(x[0], x[1], x[2], x[3])
        b2 = mol2.calctor(x[0], x[1], x[2], x[3])
        diff = b1-b2
        if diff < -180:
            diff += 360
        elif diff > 180:
            diff -= 360
        result.torsions.append(Cmprestor(x, b1, b2, diff))

    for i in range(len(mol1)):
        result.displacement.append([i, tools.distance(mol1[i], mol2[i])])

    return result

def cmpmolfile(file1, file2, cmplist = None, f1type='xyz', f2type=None):
    if f2type is None:
        f2type = f1type

    f1read = getattr(read, 'read'+f1type)
    f2read = getattr(read, 'read'+f2type)
    mol1 = f1read(file1)
    mol2 = f2read(file2)
    return cmpmol(mol1, mol2, cmplist)

def batchcmpmolfile(flist1, flist2):
    result = Batchcmpresult()
    cmplist = relalist.Relalist(read.readxyz(flist1[0]))

    for file1, file2 in zip(flist1, flist2):
        result.append(cmpmolfile(file1, file2, cmplist))

    return result

def cmpmoltop(mol1, mol2):
    "比较拓朴结构"
    if len(mol1.atoms) != len(mol2.atoms):
        return False

    for i in xrange(len(mol1.atoms)):
        if mol1.atoms[i]._no != mol2.atoms[i]._no:
            return False

    mol1.confirmconnect()
    mol2.confirmconnect()

    if mol1.connect != mol2.connect:
        return False
    else:
        return True
