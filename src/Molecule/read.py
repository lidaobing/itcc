# -*- coding: utf-8 -*-

__all__ = ['readxyz', 'readgjf', 'FormatError']

import re
from os.path import splitext
from Scientific.IO import PDB
from Scientific.Geometry import Vector
from itcc.Molecule.molecule import *
from itcc.Molecule.atom import Atom



class FormatError(Exception):
    pass

# def readmol(ifname):
#     filename, ext = splitext(ifname)

#     ext = ext.lower()
    
#     if ext == '.xyz':
#         return readxyz(ifname)
#     elif ext in ['.pdb', '.ent']:
#         return readpdb(ifname)
#     return None

# atom_format = FortranFormat('A6,I5,1X,A4,A1,A4,A1,I4,A1,3X,3F8.3,2F6.2,' +
#                             '6X,A4,2A2')
#
# conect_format = FortranFormat('A6,11I5')
# def readpdb(ifname):
#     mol = Molecule()
#     ifile = PDB.PDBFile(ifname)
#     while 1:
#         rectyp, data = ifile.readLine()
#         if rectyp == 'END':
#             break
#         elif rectyp in ['HEADER', 'MODEL', 'ENDMDL']:
#             continue
#         elif rectyp in ['ATOM', 'HETATM']:
#             atom = Atom()
#             atom.symbol = data['name'].strip()
#             atom.coords = data['position']
#             mol.atoms.append(atom)
#         elif rectyp == 'CONNECT':
#             mol.appendconnect(data['bonded'])
#     return mol

def readgjf(ifname):
    ifile = file(ifname)

    blanklines = 0
    mol = Molecule()

    while blanklines < 2:
        line = ifile.readline().strip()
        if line == '':
            blanklines += 1

    ifile.readline()  #跳过 '0 1' 这一行
      
  
    for line in ifile:
        line = line.strip()
        if line == '':
            break
        words = line.split()
        x = []
        for word in words:
            x.extend(word.split(','))
        atom = Atom(x[0])
        coords = Vector([float(coord) for coord in x[-3:]])   #可以处理两种类型的gjf: 'H 0.1 0.2 0.3' 和 'H 0 0.1 0.2 0.3'
        mol.addatom(atom, coords)
    ifile.close()
    return mol

def readxyz(ifile):
    """readxyz(ifile) => Molecule
    if got errors, raise FormatError
    """
    mol = Molecule()

    connects = []

    line = ifile.readline()
    match = re.compile(r'^ *(\d+) *(.*)$').match(line)
    atmnum = int(match.group(1))
    mol.comment = match.group(2)

    for line in ifile:
        words = line.split()
        if not words:
            break
        atom = Atom(words[1], int(words[5]))
        coord = Vector([float(x) for x in words[2:5]])
        mol.addatom(atom, coord)
        connects.append(words[6:])

    for i, connect in enumerate(connects):
        for j in connect:
            mol.buildconnect(i, int(j)-1)

    assert atmnum == len(mol)
    
    return mol

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.exit(1)
    mol = readxyz(file(sys.argv[1]))

    import write
    write.writexyz(mol, file("001.xyz", 'w'))
    
    
