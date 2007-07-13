# $Id: test_molecule_dmddat2mtxyz.py 657 2007-06-16 00:23:56Z lidaobing@gmail.com $

import unittest

from itcc.molecule import atom

class Test(unittest.TestCase):
    def test_1(self):
        a = atom.Atom(1)
        a = atom.Atom('H')
        self.assertRaises(ValueError, lambda: atom.Atom(0))
        self.assertRaises(ValueError, lambda: atom.Atom(-1))
        self.assertRaises(ValueError, lambda: atom.Atom(200))
        a = atom.Atom('HH')
        self.assertEqual(atom.Atom('Z'), atom.Atom(0, 0, 'Z'))

if __name__ == '__main__':
    unittest.main()

    
