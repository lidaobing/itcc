import math
import sys
from random import random
import numpy
from itcc.molecule import molecule, atom, write
from itcc import tinker, ccs2

CClen = 1.523

def get_c_type(n):
    if n == 3:
        return 22
    if n == 4:
        return 56
    return 1

def makecyclicalkane(n):
    assert n >= 3

    r = CClen/2.0 / math.sin(math.pi/n)
    coords = []
    for i in range(n):
        angle = math.pi * 2.0 * i / n
        coords.append([r * math.cos(angle),
                       r * math.sin(angle),
                       random()*0.1])

    mol = molecule.Molecule()
    C = atom.Atom(6, get_c_type(n))
    H = atom.Atom(1,5)
    for i in range(n):
        mol.addatom(C, coords[i])
    for i in range(n):
        mol.addatom(H, mol.coords[i] 
                       + numpy.array([random()*0.5,random()*0.5, random()*0.5]))
        mol.addatom(H, mol.coords[i] 
                       + numpy.array([random()*0.5,random()*0.5, random()*0.5]))
    for i in range(n):
        mol.buildconnect(i, (i+1)%n)
        mol.buildconnect(i, n+i*2)
        mol.buildconnect(i, n+i*2+1)
    #CCS2.shakeH(mol.coords, CCS2.getshakeHdata(mol))
    #     newmol, newene = Tinker.minimizemol(mol, "mm2")
    write.writexyz(mol, sys.stdout)

def main():
    import os
    if len(sys.argv) != 2:
        print >>sys.stderr, 'Usage: %s number' % os.path.basename(sys.argv[0])
        sys.exit(1)
    makecyclicalkane(int(sys.argv[1]))

if __name__ == '__main__':
    main()
