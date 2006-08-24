#!/usr/bin/env python

import sys
import os
import unittest
import test_base

test_methane_in = """ 5 molden generated tinker .xyz (mm3 param.)
1  C     0.000000    0.000000    0.000000      1     2    3    4    5
2  H     0.000000    0.000000    1.089000      5     1
3  H     1.026719    0.000000   -0.363000      5     1
4  H    -0.513360   -0.889165   -0.363000      5     1
5  H    -0.513360    0.889165   -0.363000      5     1
"""

test_cycc5_in = """    5 1.pdb                  MM2 parameters
     1  C    133.000000  152.000000    0.000000     1     2     4
     2  C    183.000000  152.000000    0.000000     1     1     3
     3  C    198.451000  104.447000    0.000000     1     2     5
     4  C    117.549000  104.447000    0.000000     1     1     5
     5  C    158.000000   75.058000    0.000000     1     3     4
"""

test_cycc7_in = ''' 7  cyc7.pdb               MM2 parameters
     1  C     -0.151191   -1.729547    0.000000     1     2     6
     2  C      1.257966   -1.196634    0.000000     1     1     3
     3  C      1.719796    0.237395    0.000000     1     2     7
     4  C     -0.614212    1.623928    0.000000     1     5     7
     5  C     -1.652549    0.532326    0.000000     1     4     6
     6  C     -1.446437   -0.960076    0.000000     1     1     5
     7  C      0.886626    1.492610    0.000000     1     3     4
'''

class TestConfsearch(unittest.TestCase):
    def setUp(self):
        from itcc.ccs2 import confsearch
        self.confsearch = confsearch
        os.system("rm -rf subdirs")
        os.mkdir("subdirs", 0700)
        self.olddir = os.getcwd()
        os.chdir("subdirs")
        sys.stdout = file('out', 'w')
        sys.stderr = file('err', 'w')

    def test_methane(self):
        ofile = file("test_methane.in", "w");
        ofile.write(test_methane_in)
        ofile.close()

        sys.argv = ['', 'test_methane.in']
        self.confsearch.main()

    def test_cycc5(self):
        ofile = file("test_cycc5.in", "w");
        ofile.write(test_cycc5_in)
        ofile.close()

        sys.argv = ['', 'test_cycc5.in']
        self.confsearch.main()

    def test_cycc5(self):
        ofile = file("test_cycc7.in", "w");
        ofile.write(test_cycc7_in)
        ofile.close()

        sys.argv = ['', 'test_cycc7.in']
        self.confsearch.main()

    def tearDown(self):
        os.chdir(self.olddir)

def _test():
    unittest.main()

if __name__ == '__main__':
    _test()






