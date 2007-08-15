# $Id$
import sys
import os.path
import math
from itcc.molecule import read, write
from itcc.molecule.tools import neighbours, is_pyramid
from itcc.molecule import relalist

try:
    sorted
except:
    from itcc.core.tools import sorted_ as sorted

def mirrormol():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s <xyzfname>\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    mol = read.readxyz(file(sys.argv[1]))
    mol.coords = -mol.coords
    write.writexyz(mol)

def printbonds():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s <xyzfname>\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    mol = read.readxyz(file(sys.argv[1]))
    a = relalist.Relalist(mol)
    print a

def detailcmp():
    from optparse import OptionParser
    usage = '%prog [options] <xyzfname1> <xyzfname2>'
    parser = OptionParser(usage=usage)
    
    parser.add_option('-a', "--atoms", dest="atoms",
                      help="only compare selected atoms, 1-based",
                      metavar="STRING")
    parser.add_option('-A', "--atomsfile", dest="atomsfile",
                      help="read the selected atoms from file",
                      metavar="FILE")
    
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("incorrect number of arguments")
        
    if options.atoms and options.atomsfile:
        parser.error("options conflict")
    
    if options.atomsfile:
        options.atoms = file(options.atomsfile).read()

    atoms = None
    if options.atoms:
        atoms = [int(x)-1 for x in options.atoms.split()]
        
    mol1 = read.readxyz(file(args[0]))
    mol2 = read.readxyz(file(args[1]))
    
    r1 = relalist.Relalist(mol1)
    
    bonds_data = []    
    for i,j in r1.bonds:
        if atoms is not None and (i not in atoms or j not in atoms): continue
        l1 = mol1.calclen(i,j)
        l2 = mol2.calclen(i,j)
        bonds_data.append((abs(l1-l2), (i+1,j+1), l1, l2))

    angles_data = []
    for i,j,k in r1.angles:
        if atoms is not None \
            and (i not in atoms \
                 or j not in atoms \
                 or k not in atoms):
            continue
        
        a1 = math.degrees(mol1.calcang(i,j,k))
        a2 = math.degrees(mol2.calcang(i,j,k))
        angles_data.append((abs(a1-a2), (i+1,j+1,k+1), a1, a2))

    
    torsions_data = []
    for i,j,k,l in r1.torsions:
        if atoms is not None \
            and (i not in atoms \
                 or j not in atoms \
                 or k not in atoms
                 or l not in atoms):
            continue
        t1 = math.degrees(mol1.calctor(i,j,k,l))
        t2 = math.degrees(mol2.calctor(i,j,k,l))
        torsions_data.append((180-abs(abs(t1-t2)-180), (i+1,j+1,k+1,l+1), t1, t2))

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
        print x[1][0], x[1][1], x[1][2], x[1][3], x[2], x[3], x[0]

def rg():
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s XYZFNAME...\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    from itcc.molecule import radius_of_gyration
    for fname in sys.argv[1:]:
        ifile = sys.stdin
        if fname != '-':
            ifile = file(fname)
        mol = read.readxyz(ifile)
        print ifile.name, radius_of_gyration(mol)

def sub_pyramid_check(fname, atoms):
    mol = read.readxyz(file(fname))
    if atoms is None:
        atoms = range(len(mol))
    res = []
    for atom in atoms:
        neis = neighbours(mol, atom)
        if len(neis) != 4:
            continue
        if is_pyramid(mol.coords[atom],
                      mol.coords[neis[0]],
                      mol.coords[neis[1]],
                      mol.coords[neis[2]],
                      mol.coords[neis[3]]):
            res.append(atom)
    return res

def pyramid_check():
    from optparse import OptionParser
    usage = '%prog [options] <xyzfname>...'
    parser = OptionParser(usage=usage)
    
    parser.add_option('-a', "--atoms", dest="atoms",
                      help="only compare selected atoms, 1-based",
                      metavar="STRING")
    parser.add_option('-A', "--atomsfile", dest="atomsfile",
                      help="read the selected atoms from file",
                      metavar="FILE")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("incorrect number of arguments")
        
    if options.atoms and options.atomsfile:
        parser.error("options conflict")
    
    if options.atomsfile:
        options.atoms = file(options.atomsfile).read()

    atoms = None
    if options.atoms:
        atoms = [int(x)-1 for x in options.atoms.split()]

    for fname in args:
        res = sub_pyramid_check(fname, atoms)
        if res:
            print fname, ' '.join(str(x+1) for x in res)      

        
    
        

