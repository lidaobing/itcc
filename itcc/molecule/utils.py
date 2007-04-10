import sys
from itcc.molecule import read, write

def mirrormol():
    if len(sys.argv) != 2:
        import os.path 
        sys.stderr.write('Usage: %s <xyzfname>\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    mol = read.readxyz(file(sys.argv[1]))
    mol.coords = [-x for x in mol.coords]
    write.writexyz(mol)
