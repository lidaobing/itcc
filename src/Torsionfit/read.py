# -*- coding: utf-8 -*-
# $Id$

import itertools
from os.path import splitext
from molecular import *
from itcc.Molecule.atom import Atom
from Scientific.IO import PDB

class FormatError(Exception):
    pass

def readmol(ifname):
    filename, ext = splitext(ifname)

    ext = ext.lower()
    
    if ext == '.xyz':
        return readxyz(ifname)
    elif ext in ['.pdb', '.ent']:
        return readpdb(ifname)
    return None
# atom_format = FortranFormat('A6,I5,1X,A4,A1,A4,A1,I4,A1,3X,3F8.3,2F6.2,' +
#                             '6X,A4,2A2')
#
# conect_format = FortranFormat('A6,11I5')
def readpdb(ifname):
    mol = Molecular()
    ifile = PDB.PDBFile(ifname)
    while 1:
        rectyp, data = ifile.readLine()
        if rectyp == 'END':
            break
        elif rectyp in ['HEADER', 'MODEL', 'ENDMDL']:
            continue
        elif rectyp in ['ATOM', 'HETATM']:
            atom = Atom()
            atom.symbol = data['name'].strip()
            atom.coords = data['position']
            mol.atoms.append(atom)
        elif rectyp == 'CONNECT':
            mol.appendconnect(data['bonded'])
    return mol

def readgjf(ifname):
    ifile = file(ifname)

    blanklines = 0
    mol = Molecular()

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
        words = list(itertools.chain(*[word.split(',') for word in words]))
        atom = Atom()
        atom.symbol = words[0]
        atom.coords = words[-3:]   #可以处理两种类型的gjf: 'H 0.1 0.2 0.3' 和 'H 0 0.1 0.2 0.3'
        mol.atoms.append(atom)
    ifile.close()
    return mol

def readxyz(ifile):
    """readxyz(ifile) => Molecular
    if got errors, raise FormatError
    """
    import types
    if type(ifile) in types.StringTypes:
        ifile = file(ifile)
    
    mol = Molecular()

    try:
        ifile.readline()

        for line in ifile:
            words = line.split()
            if not words:
                break
            atom = Atom()
            atom.symbol = words[1]
            atom.coords = words[2:5]
            atom.type = words[5]
            mol.atoms.append(atom)
            mol.appendconnect(words[6:])
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise FormatError
    return mol

def readxyz_2(ifname):
    
    ifile = file(ifname)
    lines = ifile.readlines()
    ifile.close()

    words = [x.split() for x in lines]
    xyz = [x[2:5] for x in words[1:]]
    return [[float(y) for y in x] for x in xyz]

def readconns(ifname):
    ifile = file(ifname)
    lines = ifile.readlines()
    ifile.close()

    words = [x.split() for x in lines]
    conns = [x[6:] for x in words[1:]]
    return [[int(y) for y in x] for x in conns]

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.exit(1)
    mol = readmol(sys.argv[1])

    import write
    write.writexyz(mol, "001.xyz")
    
    
