import numpy
import math

def radius_of_gyration(mol):
    '''return the radius of gyration of molecule'''
    if len(mol) == 0:
        return 0.0
    
    sum_coords = numpy.array([0.0, 0.0, 0.0])
    sum_mass = 0.0
    for i in range(len(mol)):
        sum_mass += mol.atoms[i].mass
        sum_coords += mol.atoms[i].mass * mol.coords[i]
    sum_coords /= sum_mass

    res = 0.0
    for i in range(len(mol)):
        res += sum((mol.coords[i] - sum_coords) ** 2) * mol.atoms[i].mass
    return math.sqrt(res/sum_mass)
    
        
