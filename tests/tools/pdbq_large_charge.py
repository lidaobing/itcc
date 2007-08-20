# $Id$

import unittest

class Test(unittest.TestCase):
    def test_1(self):
        from itcc.tools import pdbq_large_charge
        import glob
        import sys
        import os.path
        dir = os.path.split(sys.modules[__name__].__file__)[0]
        for fname in glob.glob(os.path.join(dir, 'pdbq_large_charge', '*.pdbq')):
            pdbq_large_charge.pdbq_large_charge(file(fname), 
                
        

if __name__ == '__main__':
    unittest.main()
