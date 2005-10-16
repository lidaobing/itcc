import unittest
from itcc.Molecule import read
from itcc.CCS2 import sidechain

class TestSidechain(unittest.TestCase):
    def testsidechain(self):
        mol = read.readxyz(file('sidechain-methane.xyz'))
        coords1 = mol.coords
        coords2 = coords1[0:1] + coords1[3:] + coords1[1:3]
        newcoords = sidechain.movesidechain(coords1, coords2, (0,1,2), (3,4))
        self.assert_((newcoords[3] - coords2[3]).length() < 0.001)
        self.assert_((newcoords[4] - coords2[4]).length() < 0.001)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
