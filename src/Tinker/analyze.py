# $Id$

from itcc.Molecule import relalist
from itcc.Tinker import molparam

__revision__ = '$Rev$'

def gettortype(mol, tor):
    assert len(tor) == 4
    return tuple([mol.atoms[idx].type for idx in tor])

def gettorsbytype(mol, types):
    types = map(molparam.torsion_uni, types)
    
    result = {}
    for typ in types:
        result[typ] = []
        
    mol.confirmconnect()
    tors = relalist.genD(relalist.genconns(mol.connect))
    for tor in tors:
        typ = molparam.torsion_uni(gettortype(mol, tor))
        if typ in types:
            result[typ].append(tor)
    return result
        
    
    
