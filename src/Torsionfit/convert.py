# $Id$

from itcc.Molecule import read, write

def gjf2xyz(ifname, ofname, types = None, neworder = None):
    mol = read.readgjf(ifname)
    if neworder is not None:
        mol.changeorder(neworder)
    mol.confirmconnect()
    if types is not None:
        mol.settypes(types)
    
    write.writexyz(mol, ofname)
    
