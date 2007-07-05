import unittest
import numpy
from itcc.ccs2 import sidechain
from itcc.core.tools import distance

class Test(unittest.TestCase):
    def runTest(self):
        fromcoords = numpy.array(((-1.0, 0.0, 0.0),
                                  (0.0, 0.0, 0.0),
                                  (0.0, -1.0, 0.0),
                                  (1.0, 1.0, 0.0)))
        tocoords = numpy.array(((-1.0, 0.0, 0.0),
                                (-1.0, -1.0, 0.0),
                                (0.0, -1.0, 0.0),
                                (1.0, 1.0, 0.0)))
        refidxs = (0, 1, 2)
        s = (3,)
        res = sidechain.movesidechain(fromcoords, tocoords, refidxs, s)
        self.assertAlmostEqual(distance(res[3], numpy.array((-2.0, -2.0, 0))),
                               0.0)

def _test():
    unittest.main()

if __name__ == '__main__':
    _test()
