import unittest
import numpy
from itcc.ccs2 import pyramid

class Test(unittest.TestCase):
    def test_1(self):
        A = numpy.array((1.0, 2.0, 3.0))
        B = numpy.array((5.0, 4.0, 7.0))
        C = numpy.array((-1.0, 2.0, 0.5))

        trans, revtrans = pyramid.construct_both_transform_matrix(A, B, C)
        A2 = trans(A)
        B2 = trans(B)
        C2 = trans(C)
        
        self.assertAlmostEqual(A2[0], 0.0)
        self.assertAlmostEqual(A2[1], 0.0)
        self.assertAlmostEqual(A2[2], 0.0)
        self.assertAlmostEqual(B2[1], 0.0)
        self.assertAlmostEqual(B2[2], 0.0)
        self.assertAlmostEqual(C2[2], 0.0)

        A3 = revtrans(A2)
        B3 = revtrans(B2)
        C3 = revtrans(C2)
        for i in range(3):
            self.assertAlmostEqual(A[i], A3[i])
            self.assertAlmostEqual(B[i], B3[i])
            self.assertAlmostEqual(C[i], C3[i])



if __name__ == '__main__':
    unittest.main()
