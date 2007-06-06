import sys
import os.path
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
    
    import relalist
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
        print x

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
        
    
        

