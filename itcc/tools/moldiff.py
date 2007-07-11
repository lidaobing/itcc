# $Id$

import sys

from itcc.molecule import read

def moldiff(mol1, mol2):
    assert len(mol1) == len(mol2)
    return [sum((mol1.coords[i] - mol2.coords[i])**2)**0.5
            for i in range(len(mol1))]

def main():    
    if len(sys.argv) != 3:
        import os.path
        sys.stderr.write('Usage: %s mol1fname mol2fname\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    mol1_ifile = sys.stdin
    if sys.argv[1] != '-':
        mol1_ifile = file(sys.argv[1])
    mol1 = read.readxyz(mol1_ifile)
    
    mol2_ifile = sys.stdin
    if sys.argv[2] != '-':
        mol2_ifile = file(sys.argv[2])
    mol2 = read.readxyz(mol2_ifile)
    
    res = moldiff(mol1, mol2)
    
    for i, x in enumerate(res):
        print i+1, '%f' % x
    
if __name__ == '__main__':
    main()
    