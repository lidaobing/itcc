import os
import os.path
import unittest
from itcc.Molecule import read
from itcc.CCS2 import sidechain

class TestConfsearchCA(unittest.TestCase):
    def test(self):
        os.system('rm -f cycC9.*')
        os.system('python2.4 makecyclicalkane.py 9 > cycC9.xyz')
        self.assert_(os.system('confsearch.py -f mm3 cycC9.xyz > cycC9.log') == 0)
        self.assert_(os.path.exists('cycC9.007'))
        self.assert_(not os.path.exists('cycC9.008'))
        os.system('rm -f cycC9.*')

def main():
    unittest.main()

if __name__ == '__main__':
    main()
