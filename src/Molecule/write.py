# $Id$

from itcc.Molecule.molecule import *
from itcc.Molecule.atom import atomchr

__revision__ = '$Rev$'

def writexyz(mol, ofile, comment=None):
    assert(isinstance(mol, Molecule))

    mol.confirmconnect()

    ofile.write('%6i' % len(mol))
    if comment is not None:
        ofile.write(' %s' % comment)
    elif hasattr(mol, 'comment'):
        ofile.write(' %s' % mol.comment)
    ofile.write('\n')
        
    for i in range(len(mol)):
        atom, coord = mol[i]
        tmpstr = '%6d  %-2s %12.6f%12.6f%12.6f%6s' % \
                 (i+1, atom.symbol, coord.x(), coord.y(), coord.z(), atom.type)
        for j, x in enumerate(mol.connect[i]):
            if x:
                tmpstr += '%6i' % (j+1)
        tmpstr += '\n'
        ofile.write(tmpstr)

gjfheader ='#p b3lyp/6-31g* opt\n'
gjfcomment = 'notitle\n'
gjfchargespin = '0 1\n'

def writegjf(mol, ofile):
    assert(isinstance(mol, Molecule))
    ofile.write(gjfheader)
    ofile.write('\n')
    ofile.write(gjfcomment)
    ofile.write('\n')
    ofile.write(gjfchargespin)
    for i in range(len(mol)):
        atom, coord = mol[i]
        ofile.write('%s %f %f %f\n' % (atomchr(atom.no), coord.x(),
            coord.y(), coord.z()))
    ofile.write('\n')

    


        
    
    
