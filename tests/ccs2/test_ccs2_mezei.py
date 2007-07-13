import math
import unittest
import numpy
import pprint
import warnings
from itcc.ccs2 import mezei
from itcc.core.tools import distance

class Test(unittest.TestCase):
    def runTest(self):
        points = numpy.array(((0.0, 0.0, 0.0),
                              (1.0, 0.0, 0.0),
                              (2.0, 2.0, 1.0),
                              (2.0, 2.0, 2.0)))
        len1 = numpy.array((1.0, 1.0, 1.0, 1.0))
        len2 = numpy.array((math.sqrt(2.0),)*5)

        a = tuple(mezei.r6_base(points, len1, len2, 1e-9))

        self.assert_(len(a) >= 4, str(a))
        if len(a) != 6:
            warnings.warn("this testcase should return 6 result")

        for x in a:
            self.assertAlmostEqual(distance(points[1], x[2]), 1.0)
            self.assertAlmostEqual(distance(x[2], x[3]), 1.0)
            self.assertAlmostEqual(distance(x[4], points[2]), 1.0)
            self.assertAlmostEqual(distance(x[3], x[4]), 1.0)
            self.assertAlmostEqual(distance(points[0], x[2]), math.sqrt(2.0))
            self.assertAlmostEqual(distance(points[1], x[3]), math.sqrt(2.0))
            self.assertAlmostEqual(distance(x[2], x[4]), math.sqrt(2.0))
            self.assertAlmostEqual(distance(x[3], points[2]), math.sqrt(2.0))
            self.assertAlmostEqual(distance(x[4], points[3]), math.sqrt(2.0))

        for i in range(len(a)):
            for j in range(i):
                self.assert_(sum([distance(a[i][k], a[j][k]) for k in range(2,5)]) > 0.5)

def _test():
    unittest.main()

if __name__ == '__main__':
    _test()
