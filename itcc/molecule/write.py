# $Id$

import sys
from itcc.molecule.molecule import Molecule
from itcc.molecule.atom import atomchr
from itcc.molecule.pdb import write as writepdb

__revision__ = '$Rev$'
__all__ = ['writepdb', 'writexyz', 'writegjf']

def writexyz(mol, ofile=sys.stdout, comment=None):
    assert(isinstance(mol, Molecule))

    mol.confirmconnect()

    ofile.write('%6i' % len(mol))
    if comment is not None:
        ofile.write('  %s' % comment)
    elif hasattr(mol, 'comment') and mol.comment:
        ofile.write('  %s' % mol.comment)
    ofile.write('\n')

    for i in range(len(mol)):
        atom, coord = mol[i]
        tmpstr = '%6d  %-3s%12.6f%12.6f%12.6f%6s' % \
                 (i+1, atom.symbol, coord[0], coord[1], coord[2], atom.type)
        for j, x in enumerate(mol.connect[i]):
            if x:
                tmpstr += '%6i' % (j+1)
        tmpstr += '\n'
        ofile.write(tmpstr)

gjfheader = '''\
#p b3lyp/6-31g* opt

notitle

0 1
'''

def writegjf(mol,
             ofile = sys.stdout,
             header = None
             ):
    if header is None:
        header = gjfheader
    assert(isinstance(mol, Molecule))
    ofile.write(header)
    for i in range(len(mol)):
        atom, coord = mol[i]
        ofile.write('%s %f %f %f\n' % (atomchr(atom.no), coord[0],
            coord[1], coord[2]))
    ofile.write('\n')
