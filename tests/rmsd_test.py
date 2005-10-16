import unittest
from itcc.Molecule import _rmsd, read

class TestRMSD(unittest.TestCase):
    def testrmsd(self):
        mol1 = read.readxyz(file('rmsd.1.xyz'))
        mol2 = read.readxyz(file('rmsd.2.xyz'))
        self.assert_(abs(_rmsd.rmsd(mol1, mol2) - 1.001) < 0.001)

def main():
    unittest.main()

if __name__ == '__main__':
    main()


