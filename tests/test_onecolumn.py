# $Id$

import unittest
import test_base
import StringIO
from itcc.tools import onecolumn

test_in = "1 2\n3 4\n"
test_out = "1\n2\n3\n4\n"

class TestOnecolumn(unittest.TestCase):
    def test(self):
        ifile = StringIO.StringIO(test_in)
        ofile = StringIO.StringIO()
        onecolumn.onecolumn(ifile, ofile)
        self.assertEqual(ofile.getvalue(), test_out)

if __name__ == '__main__':
    unittest.main()
