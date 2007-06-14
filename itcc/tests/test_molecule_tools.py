import unittest
import StringIO

from itcc.molecule import read, tools

test_methane_in = """ 5 molden generated tinker .xyz (mm3 param.)
1  C     0.000000    0.000000    0.000000      1     2    3    4    5
2  H     0.000000    0.000000    1.089000      5     1
3  H     1.026719    0.000000   -0.363000      5     1
4  H    -0.513360   -0.889165   -0.363000      5     1
5  H    -0.513360    0.889165   -0.363000      5     1
"""

class Test(unittest.TestCase):
    def runTest(self):
        mol = read.readxyz(StringIO.StringIO(test_methane_in))
        neighbours = tools.neighbours(mol, 0)
        neighbours.sort()
        neighbours = tuple(neighbours)
        self.assertEqual(neighbours, (1,2,3,4))

def _test():
    unittest.main()

if __name__ == '__main__':
    _test()
