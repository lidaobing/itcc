import math
import sys
from random import random
from itcc.Molecule import molecule, atom, write
from itcc.Tinker import tinker
from itcc import CCS2
from Scientific.Geometry import Vector


CClen = 1.523

def randomvector(len_ = 1.0):
    result = Vector(random(), random(), random())
    return result.normal()*len_

def makecyclicalkane(n):
    if n < 3:
        return

    r = CClen/2.0 / math.sin(math.pi/n)
    coords = []
    for i in range(n):
        angle = math.pi * 2.0 * i / n
        coords.append(Vector(r * math.cos(angle), r * math.sin(angle),
          random()*0.1))

    mol = molecule.Molecule()
    C = atom.Atom(6,1)
    H = atom.Atom(1,5)
    for i in range(n):
        mol.addatom(C, coords[i])
    for i in range(n):
        mol.addatom(H, randomvector() + coords[i])
        mol.addatom(H, randomvector() + coords[i])
    for i in range(n):
        mol.buildconnect(i, (i+1)%n)
        mol.buildconnect(i, n+i*2)
        mol.buildconnect(i, n+i*2+1)
    # CCS2.shakeH(mol.coords, CCS2.getshakeHdata(mol))
    newmol, newene = tinker.minimizemol(mol, "mm3")
    write.writexyz(newmol, sys.stdout, newene)

def main():
    import os
    if len(sys.argv) != 2:
        print >>sys.stderr, 'Usage: %s number' % os.path.basename(sys.argv[0])
        sys.exit(1)
    makecyclicalkane(int(sys.argv[1]))

if __name__ == '__main__':
    main()
