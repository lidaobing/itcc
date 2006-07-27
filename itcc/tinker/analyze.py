# $Id$

from itcc.molecule import relalist
from itcc.tinker import molparam

__revision__ = '$Rev$'

def gettortype(mol, tor):
    assert len(tor) == 4
    return tuple([mol.atoms[idx].type for idx in tor])


def gettorsbytype(mol, types):
    types = [molparam.torsion_uni(type_) for type_ in types]

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



