import unittest

from itcc.core import frame

class Test(unittest.TestCase):
    def test_1(self):
        self.assertEqual(tuple(frame.parseframe('1,2')), (0,1))
        self.assertEqual(tuple(frame.parseframe('1-3')), (0,1,2))
        self.assertEqual(tuple(frame.parseframe('1-3/2')), (0,2))
        self.assertEqual(tuple(frame.parseframe('3/2')), (2,))
        self.assertEqual(tuple(frame.parseframe(None)), ())

if __name__ == '__main__':
    unittest.main()
