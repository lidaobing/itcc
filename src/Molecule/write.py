from itcc.Molecule.molecule import *

def writexyz(mol, ofile, comment=None):
    assert(isinstance(mol, Molecule))

    ofile.write('%6i' % len(mol))
    if comment is not None:
        ofile.write(' %s' % comment)
    elif hasattr(mol, 'comment'):
        ofile.write(' %s' % mol.comment)
    ofile.write('\n')
        
    for i in range(len(mol)):
        atom, coord = mol[i]
        tmpstr = '%6d  %-2s %12.6f%12.6f%12.6f%6s' %\
                 (i+1, atom.symbol, coord.x(), coord.y(), coord.z(), atom.type)
        for j, x in enumerate(mol.connect[i]):
            if x:
                tmpstr += '%6i' % (j+1)
        tmpstr += '\n'
        ofile.write(tmpstr)


        
    
    
