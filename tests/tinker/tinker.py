import unittest

from StringIO import StringIO
from itcc.molecule import read
from itcc.tinker import tinker

test_in = ''' 5 molden generated tinker .xyz (mm3 param.)
    1  C     0.000000    0.000000    0.000000      1     2    3    4    5
    2  H     0.000000    0.000000    1.089000      5     1
    3  H     1.026719    0.000000   -0.363000      5     1
    4  H    -0.513360   -0.889165   -0.363000      5     1
    5  H    -0.513360    0.889165   -0.363000      5     1
'''

class Test(unittest.TestCase):
    def test(self):
        mol = read.readxyz(StringIO(test_in))
        self.assertAlmostEqual(tinker.analyze(mol, "mm2"), 0.7996)

if __name__ == '__main__':
    unittest.main()
