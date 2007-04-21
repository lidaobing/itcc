# $Id$

import unittest
import numpy
from itcc.molecule import read
from itcc.ccs2 import sidechain
from itcc.tools import tools

test_in = '''\
 5 molden generated tinker .xyz (mm3 param.)
    1  C     0.000000    0.000000    0.000000      1     2    3    4    5
    2  H     0.000000    0.000000    1.089000      5     1
    3  H     1.026719    0.000000   -0.363000      5     1
    4  H    -0.513360   -0.889165   -0.363000      5     1
    5  H    -0.513360    0.889165   -0.363000      5     1
'''

class TestSidechain(unittest.TestCase):
    def testsidechain(self):
        import StringIO
        mol = read.readxyz(StringIO.StringIO(test_in))
        coords1 = mol.coords
        coords2 = coords1.copy()
        coords2[1] = coords1[3]
        coords2[2] = coords1[4]
        coords2[3] = coords1[1]
        coords2[4] = coords1[2]
        newcoords = sidechain.movesidechain(coords1, coords2,
                                            (0, 1, 2),
                                            (3, 4))
        for key in newcoords:
            coord = newcoords[key]
            assert isinstance(coord, numpy.ndarray) and coord.shape == (3,) and coord.dtype == float, (coord, coord.shape, coord.dtype)
        self.assertAlmostEqual(tools.length(newcoords[3] - coords2[3]), 0, 4)
        self.assertAlmostEqual(tools.length(newcoords[4] - coords2[4]), 0, 4)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
