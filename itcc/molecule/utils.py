import sys
import math
from itcc.molecule import read, write

def mirrormol():
    if len(sys.argv) != 2:
        import os.path 
        sys.stderr.write('Usage: %s <xyzfname>\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    mol = read.readxyz(file(sys.argv[1]))
    mol.coords = [-x for x in mol.coords]
    write.writexyz(mol)

def printbonds():
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s <xyzfname>\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    mol = read.readxyz(file(sys.argv[1]))
    import relalist
    a = relalist.Relalist(mol)
    print a

def detailcmp():
    if len(sys.argv) != 3:
        import os.path
        sys.stderr.write('Usage: %s <xyzfname1> <xyzfname2>\n'
                         % os.path.basename(sys.argv[0]))
        sys.exit(1)
    mol1 = read.readxyz(file(sys.argv[1]))
    mol2 = read.readxyz(file(sys.argv[2]))

    import relalist
    r1 = relalist.Relalist(mol1)
    
    bonds_data = []    
    for i,j in r1.bonds:
        l1 = mol1.calclen(i,j)
        l2 = mol2.calclen(i,j)
        bonds_data.append((abs(l1-l2), (i,j), l1, l2))

    angles_data = []
    for i,j,k in r1.angles:
        a1 = math.degrees(mol1.calcang(i,j,k))
        a2 = math.degrees(mol2.calcang(i,j,k))
        angles_data.append((abs(a1-a2), (i,j,k), a1, a2))

    
    torsions_data = []
    for i,j,k,l in r1.torsions:
        t1 = math.degrees(mol1.calctor(i,j,k,l))
        t2 = math.degrees(mol2.calctor(i,j,k,l))
        torsions_data.append((180-abs(abs(t1-t2)-180), (i,j,k,l), t1, t2))

    print 'bonds:'
    for x in sorted(bonds_data):
        print x

    print
    print 'angles:'
    for x in sorted(angles_data):
        print x

    print
    print 'torsions:'
    for x in sorted(torsions_data):
        print x
        

