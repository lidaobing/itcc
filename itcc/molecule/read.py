# $Id$
# -*- coding: utf-8 -*-

__all__ = ['readxyz', 'readgjf', 'FormatError']
__revision__ = '$Rev$'

import re
from itcc.molecule.molecule import Molecule
from itcc.molecule.atom import Atom



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

def readgjf(ifile_or_ifname):
    if isinstance(ifile_or_ifname, str):
        ifile = file(ifile_or_ifname)
    else:
        ifile = ifile_or_ifname

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
        #Can deal with two types gjf file: 'H 0.1 0.2 0.3' and 'H 0 0.1 0.2 0.3'
        coord = [float(coord) for coord in x[-3:]]   
        mol.addatom(atom, coord)
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
    comment = match.group(2).strip()
    if comment:
        mol.comment = comment

    for i in range(atmnum):
        words = ifile.readline().split()
        atom = Atom(words[1], int(words[5]))
        coord = [float(x) for x in words[2:5]]
        mol.addatom(atom, coord)
        connects.append(words[6:])

    for i, connect in enumerate(connects):
        for j in connect:
            mol.buildconnect(i, int(j)-1)

    assert atmnum == len(mol)
    
    return mol

    
    
