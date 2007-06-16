import unittest
import numpy
import math
from itcc.tools import tools

class TestTools(unittest.TestCase):
    def test_torsionangle(self):
        a = numpy.array((0.0, 0.0, 0.0))
        b = numpy.array((1.0, 0.0, 0.0))
        c = numpy.array((1.0, 1.0, 0.0))
        d = numpy.array((1.0, 1.0, 1.0))
        
        t1 = tools.torsionangle(a, a, c, d)
        self.assertNotEqual(t1, t1) # t1 is nan
        t1 = tools.torsionangle(a, b, b, d)
        self.assertNotEqual(t1, t1) # t1 is nan
        t1 = tools.torsionangle(a, b, c, c)
        self.assertNotEqual(t1, t1) # t1 is nan
        t1 = tools.torsionangle(a, b, a, d)
        self.assertNotEqual(t1, t1) # t1 is nan
        t1 = tools.torsionangle(a, b, c, b)
        self.assertNotEqual(t1, t1) # t1 is nan
        self.assertAlmostEqual(math.degrees(tools.torsionangle(a, b, c, a)),
                               0.0)
        self.assertAlmostEqual(math.degrees(tools.torsionangle(a, b, c, d)),
                               90.0)

def _test():
    unittest.main()

if __name__ == '__main__':
    _test()
        
