# $Id$
import random
import math
from itcc import Molecular, CCS2, Tinker, Tools
from Scientific.Geometry import Vector

FF_MM2 = 'mm2'
FF_MM3 = 'mm3'
FF_OPLSAA = 'oplsaa'

def gettype_MM2(n):
    if n == 3:
        return 22,5
    else:
        return 1,5

def gettype_MM3(n):
    if n == 3:
        return 22,5
    if n == 4:
        return 56,5
    return 1,5

def gettype_OPLSAA(_):
    return 2,6



class CycloAlkane:
    CClen = 1.523
    CHlen = 1.113
    CCCangle = math.radians(109.5)
    forcefield = FF_MM2
    gettypefun = {FF_MM2:gettype_MM2}
    
    def gettype(self, forcefield, n):
        return self.gettypefun[forcefield](n)

    def setforcefield(self, forcefield):
        self.forcefield = forcefield

    def makebyrandom(self, n):
        '''return a Molecular object'''
        forcefield = self.forcefield
        
        if n < 3:
            raise ValueError
        Ctype, Htype = self.gettype(forcefield, n)

        r = self.CClen/2.0 / math.sin(math.pi/n)
        coords = []
        for i in range(n):
            angle = math.pi * 2.0 * i / n
            coords.append(Vector(r * math.cos(angle), r * math.sin(angle), random.random()*0.1))

        mol = Molecular.Molecular()
        C = Molecular.Atom(6,Ctype)
        H = Molecular.Atom(1,Htype)
        for i in range(n):
            mol.addatom(C, coords[i])
        for i in range(2*n):
            mol.addatom(H, Vector(0.0, 0.0, 0.0))
        for i in range(n):
            mol.buildconnect(i, (i+1)%n)
            mol.buildconnect(i, n+i*2)
            mol.buildconnect(i, n+i*2+1)
        CCS2.shakeH(mol.coords, CCS2.getshakeHdata(mol))
        newmol, newene = Tinker.minimizemol(mol, forcefield)
        return newmol
    
    def makebytors(self, tors):
        forcefield = self.forcefield
        n = len(tors) + 3

        Ctype, Htype = self.gettype(forcefield, n)
        C = Molecular.Atom(6,Ctype)
        H = Molecular.Atom(1,Htype)

        coords = [None] * n
        coords[0] = Vector(self.CClen, 0.0, 0.0)
        coords[1] = Vector(0.0, 0.0, 0.0)
        coords[2] = Vector(self.CClen * math.cos(self.CCCangle),
                           self.CClen * math.sin(self.CCCangle), 0.0)
        for i in range(3, n):
            coords[i] = Tools.xyzatm(coords[i-1], coords[i-2], coords[i-3],
                                     self.CClen, self.CCCangle, tors[i-3])

        mol = Molecular.Molecular()
        for coord in coords:
            mol.addatom(C, coord)
        for i in range(2*n):
            mol.addatom(H, Vector(0.0, 0.0, 0.0))
        for i in range(n):
            mol.buildconnect(i, (i+1)%n)
            mol.buildconnect(i, n+i*2)
            mol.buildconnect(i, n+i*2+1)
        CCS2.shakeH(mol.coords, CCS2.getshakeHdata(mol))
        return mol
        
_cycloalkane = CycloAlkane()
makebyrandom = _cycloalkane.makebyrandom
makebytors = _cycloalkane.makebytors


