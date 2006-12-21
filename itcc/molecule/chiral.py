# $Id$

def chiral_type(mol, idx):
    if mol.connect is None: return None
    connects = [i for i in range(len(mol)) if mol.connect[idx, i]]
    if len(connects) != 4: return None
    return mol.calctor(*connects) > 0.0 
