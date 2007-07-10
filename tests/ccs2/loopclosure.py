# $Id$
import unittest

from itcc.ccs2 import loopclosure

class Test(unittest.TestCase):
    def test_1(self):
        self.assert_(callable(loopclosure.LoopClosure(loopclosure.LoopClosure.get_default_config())))

if __name__ == '__main__':
    unittest.main()
