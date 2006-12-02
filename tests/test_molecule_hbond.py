import unittest
import StringIO

from itcc.molecule import read, hbond

test_in = ''' 50  -125.3756
     1  N      0.845907   -0.569507    1.239074    85     2     5    43
     2  CT     1.414650    0.476344    2.075648    74     1     3     6     7
     3  C      2.840304    0.061309    2.476966    82     2     4    11
     4  O      3.049506   -0.550096    3.525847    83     3
     5  H      0.270442   -1.275660    1.692130    88     1
     6  HC     1.466201    1.405063    1.503587     6     2
     7  CT     0.507589    0.712728    3.294321     1     2     8     9    10
     8  HC    -0.484071    1.045758    2.987802     6     7
     9  HC     0.924924    1.478953    3.948672     6     7
    10  HC     0.385826   -0.195191    3.887159     6     7
    11  N      3.808210    0.352666    1.598630    85     3    12    15
    12  CT     5.246142    0.072168    1.675091    74    11    13    16    17
    13  C      5.585345   -1.418253    1.511868    82    12    14    21
    14  O      6.408138   -1.768700    0.671669    83    13
    15  H      3.478862    0.711663    0.709696    88    11
    16  HC     5.683114    0.574939    0.810881     6    12
    17  CT     5.899701    0.682961    2.929347     1    12    18    19    20
    18  HC     6.981047    0.541568    2.907118     6    17
    19  HC     5.711341    1.754711    2.989441     6    17
    20  HC     5.533300    0.226005    3.848859     6    17
    21  N      4.950641   -2.280666    2.312145    85    13    22    25
    22  CT     5.067409   -3.733378    2.258854    74    21    23    26    27
    23  C      3.749452   -4.308816    1.728246    82    22    24    31
    24  O      3.670734   -4.749077    0.583677    83    23
    25  H      4.268242   -1.864251    2.939636    88    21
    26  HC     5.858762   -4.036366    1.569362     6    22
    27  CT     5.417679   -4.265416    3.660303     1    22    28    29    30
    28  HC     4.698917   -3.950342    4.417173     6    27
    29  HC     5.454220   -5.355637    3.665373     6    27
    30  HC     6.399529   -3.907529    3.971460     6    27
    31  N      2.689316   -4.280094    2.546242    85    23    32    35
    32  CT     1.351550   -4.753177    2.194109    74    31    33    36    37
    33  C      0.604779   -3.629177    1.460749    82    32    34    41
    34  O     -0.320543   -3.028862    2.006182    83    33
    35  H      2.805345   -3.844459    3.447681    88    31
    36  HC     1.422902   -5.609451    1.519765     6    32
    37  CT     0.625654   -5.214089    3.470198     1    32    38    39    40
    38  HC    -0.379622   -5.568514    3.238063     6    37
    39  HC     0.526459   -4.403927    4.194077     6    37
    40  HC     1.157536   -6.034062    3.952844     6    37
    41  N      1.061420   -3.308153    0.241110    85    33    42    45
    42  CT     0.690027   -2.170382   -0.612135    74    41    43    46    47
    43  C      1.185556   -0.837082   -0.026341    82     1    42    44
    44  O      1.895792   -0.082674   -0.687986    83    43
    45  H      1.873524   -3.839796   -0.058498    88    41
    46  HC     1.233546   -2.314927   -1.547115     6    42
    47  CT    -0.811430   -2.144350   -0.955129     1    42    48    49    50
    48  HC    -1.028620   -1.350124   -1.670316     6    47
    49  HC    -1.433774   -1.966844   -0.077847     6    47
    50  HC    -1.128088   -3.085295   -1.404769     6    47
'''
class TestNeighbours(unittest.TestCase):
    def test_hbond(self):
        mol = read.readxyz(StringIO.StringIO(test_in))
        hbonds = set(hbond.detect_hbond(mol))
        assert hbonds == set(((33, 4, 0), (43, 14, 10), (3, 24, 20), (23, 44, 40)))

def _test():
    unittest.main()

if __name__ == '__main__':
    _test()