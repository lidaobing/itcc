#$Id$
#$Log: write.py,v $
#Revision 1.3  2004/08/13 07:21:00  nichloas
#* writexyz
#  - support ofile and ofname
#
#Revision 1.2  2003/12/02 06:58:41  nichloas
#*** empty log message ***
#
from molecular import *
import types


def writexyz(mol, ofile):
    '''
    '''
    assert(isinstance(mol, Molecular))
    if type(ofile) in types.StringTypes:
        ofile = file(ofile, 'w+')
    if not mol.connect:
        mol.buildconnect()

    ofile.write('%i\n' % len(mol))
    

    for i in range(len(mol)):
        atom = mol[i]
        tmpstr = '%5d  %-2s%12.6f%12.6f%12.6f%6s' %\
                 (i+1, atom.symbol, atom.x, atom.y, atom.z, atom.type)
        for x in mol.connect[i]:
            tmpstr += '%6i' % (x+1)
        tmpstr += '\n'
        ofile.write(tmpstr)


        
    
    
