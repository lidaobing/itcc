# $Id$

import unittest
import math

import numpy

from itcc.molecule import molecule
from itcc.molecule.atom import Atom

class Test(unittest.TestCase):
    def test_1(self):
        mol = molecule.Molecule(atoms = [Atom(1), Atom(1), Atom(1)],
                       coords = numpy.array([[0.0, 0.0, 0.0],
                                             [1.0, 0.0, 0.0],
                                             [1.0, 0.0, 0.0]]))
        self.assertEqual(str(mol.calcang(0, 1, 2)), 'nan')
        self.assertAlmostEqual(mol.calcang(1, 0, 2), 0.0)
        
        mol2 = molecule.Molecule(atoms = [Atom(1), Atom(1), Atom(1)],
                       coords = numpy.array([[0.0, 0.0, 0.0],
                                             [1.0, 0.0, 0.0],
                                             [1.0, 1.0, 0.0]]))
        self.assertAlmostEqual(mol2.calcang(0, 1, 2), math.radians(90.0))
        self.assertAlmostEqual(mol2.calcang(1, 0, 2), math.radians(45.0))       

if __name__ == '__main__':
    unittest.main()
