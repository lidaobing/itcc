# $Id$

import unittest

from itcc.tests import (test_ccs2_detectloop,
                        test_ccs2_mezei,
                        test_ccs2_pyramid,
                        test_ccs2_sidechain)

class TestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(test_ccs2_detectloop.Test())
        self.addTest(test_ccs2_mezei.Test())
        self.addTest(test_ccs2_pyramid.Test())
        self.addTest(test_ccs2_sidechain.Test())

alltests = TestSuite()        

def _test():
    unittest.main()

if __name__ == '__main__':
    _test()
