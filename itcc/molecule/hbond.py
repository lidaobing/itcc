# $Id$

import math

from itcc.molecule import tools

__all__ = ['detect_donor', 'detect_acceptor', 'detect_hbond']

def detect_donor(mol):
    '''detect_donor(mol) -> yield (H-idx, H's neighbour's idx)
    '''
    for idx, atom in enumerate(mol.atoms):
        if atom.no != 1:
            continue
        neighbours = tools.neighbours(mol, idx)
        neighbour = neighbours[0]
        if mol.atoms[neighbour].no in [7, 8, 16]:
            yield (idx, neighbour)

def detect_acceptor(mol):
    '''detect_acceptor(mol) -> yield O-idx
    '''
    for idx, atom in enumerate(mol.atoms):
        if atom.no == 8:
            yield idx

def detect_hbond(mol):
    '''detect_hbond(mol) -> yield (acceptor's idx, H-idx, H's neighbour's idx
    '''
    acceptors = tuple(detect_acceptor(mol))
    for donor in detect_donor(mol):
        for acceptor in acceptors:
            length = mol.calclen(acceptor, donor[1])
            if length > 3.1:
                continue
            angle = math.degrees(mol.calcang(acceptor, donor[0], donor[1]))
            if angle < 120.0:
                continue
            yield (acceptor, donor[0], donor[1])    


    
