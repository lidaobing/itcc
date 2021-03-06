# $Id$
import sys
import os
import unittest

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

test_cycg5_in = '''\
    42  title
     1  N      1.155310    1.801083   -0.188580    85     2     5    38
     2  CT     0.943566    0.906328    0.946078    73     1     3     6     7
     3  C      2.228954    0.206349    1.395260    82     2     4     8
     4  O      2.670834    0.377059    2.529896    83     3
     5  H      1.213198    2.799704   -0.003442    88     1
     6  HC     0.191008    0.155279    0.700421     6     2
     7  HC     0.545422    1.487512    1.778457     6     2
     8  N      2.840196   -0.577440    0.501269    85     3     9    12
     9  CT     4.030423   -1.389025    0.741188    73     8    10    13    14
    10  C      5.318339   -0.561313    0.752235    82     9    11    15
    11  O      6.209426   -0.779325   -0.066443    83    10
    12  H      2.435563   -0.589522   -0.432003    88     8
    13  HC     3.938388   -1.925288    1.687083     6     9
    14  HC     4.100107   -2.145082   -0.041544     6     9
    15  N      5.416423    0.400655    1.675359    85    10    16    19
    16  CT     6.578639    1.254048    1.907409    73    15    17    20    21
    17  C      6.708955    2.371213    0.868700    82    16    18    22
    18  O      6.669744    3.551555    1.210832    83    17
    19  H      4.592881    0.549743    2.253652    88    15
    20  HC     6.491762    1.698814    2.899268     6    16
    21  HC     7.491922    0.656832    1.911052     6    16
    22  N      6.854088    2.002188   -0.407983    85    17    23    26
    23  CT     7.065833    2.896944   -1.542641    73    22    24    27    28
    24  C      5.780444    3.596922   -1.991823    82    23    25    29
    25  O      5.338565    3.426212   -3.126459    83    24
    26  H      6.796200    1.003567   -0.593122    88    22
    27  HC     7.818391    3.647992   -1.296984     6    23
    28  HC     7.463977    2.315759   -2.375020     6    23
    29  N      5.169203    4.380711   -1.097832    85    24    30    33
    30  CT     3.978975    5.192296   -1.337751    73    29    31    34    35
    31  C      2.691059    4.364584   -1.348798    82    30    32    36
    32  O      1.799972    4.582596   -0.530121    83    31
    33  H      5.573835    4.392793   -0.164560    88    29
    34  HC     3.909291    5.948353   -0.555019     6    30
    35  HC     4.071011    5.728559   -2.283646     6    30
    36  N      2.592976    3.402616   -2.271922    85    31    37    40
    37  CT     1.430760    2.549223   -2.503973    73    36    38    41    42
    38  C      1.300443    1.432058   -1.465263    82     1    37    39
    39  O      1.339655    0.251716   -1.807395    83    38
    40  H      3.416518    3.253528   -2.850215    88    36
    41  HC     0.517477    3.146438   -2.507616     6    37
    42  HC     1.517637    2.104456   -3.495831     6    37
'''

class TestConfsearch(unittest.TestCase):
    def setUp(self):
        from itcc.ccs2 import confsearch
        self.confsearch = confsearch
        self.stdout_bak = sys.stdout
        self.stderr_bak = sys.stderr
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

    def test_cycc7(self):
        ofile = file("test_cycc7.in", "w");
        ofile.write(test_cycc7_in)
        ofile.close()

        sys.argv = ['', 'test_cycc7.in']
        self.confsearch.main()

#    def test_cycg5(self):
#        ofile = file("test_cycg5.in", "w");
#        ofile.write(test_cycg5_in)
#        ofile.close()
#
#        sys.argv = ['', '-f', 'oplsaa', '-t', 'peptide', '-m', '2', 'test_cycg5.in']
#        self.confsearch.main()
        
    def tearDown(self):
        sys.stdout = self.stdout_bak
        sys.stderr = self.stderr_bak
        os.chdir(self.olddir)

def _test():
    unittest.main()

if __name__ == '__main__':
    _test()






