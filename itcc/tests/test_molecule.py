# $Id$

import unittest

from itcc.tests import (test_molecule_dmddat2mtxyz,
                        test_molecule_hbond,
                        test_molecule_mol2top,
                        test_molecule_pickle,
                        test_molecule_rmsd,
                        test_molecule_tools)

class TestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(test_molecule_dmddat2mtxyz.Test())
        self.addTest(test_molecule_hbond.Test())
        self.addTest(test_molecule_mol2top.Test())
        self.addTest(test_molecule_pickle.Test())
        self.addTest(test_molecule_rmsd.Test())
        self.addTest(test_molecule_tools.Test())

alltests = TestSuite()        

def _test():
    unittest.main()

if __name__ == '__main__':
    _test()
