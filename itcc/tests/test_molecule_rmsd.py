import unittest
from itcc.molecule import _rmsd, read



class Test(unittest.TestCase):
    def runTest(self):
        import StringIO
        mol1 = read.readxyz(StringIO.StringIO(test_in_1))
        mol2 = read.readxyz(StringIO.StringIO(test_in_2))
        self.assertAlmostEqual(_rmsd.rmsd(mol1, mol2), 1.001, 3)

test_in_1 = '''\
    51  19.0934
     1  C      3.666000    0.063000    0.085000     1     2    17    18    19
     2  C      2.642000    1.092000   -0.428000     1     1     3    20    21
     3  C      2.396000    2.254000    0.546000     1     2     4    22    23
     4  C      1.676000    3.457000   -0.085000     1     3     5    24    25
     5  C      0.315000    3.161000   -0.737000     1     4     6    26    27
     6  C     -0.726000    2.546000    0.213000     1     5     7    28    29
     7  C     -2.132000    2.568000   -0.411000     1     6     8    30    31
     8  C     -3.223000    1.922000    0.459000     1     7     9    32    33
     9  C     -3.089000    0.404000    0.679000     1     8    10    34    35
    10  C     -3.061000   -0.403000   -0.629000     1     9    11    36    37
    11  C     -3.175000   -1.925000   -0.433000     1    10    12    38    39
    12  C     -2.114000   -2.559000    0.482000     1    11    13    40    41
    13  C     -0.670000   -2.221000    0.080000     1    12    14    42    43
    14  C      0.361000   -3.001000    0.913000     1    13    15    44    45
    15  C      1.783000   -2.430000    0.773000     1    14    16    46    47
    16  C      1.993000   -1.176000    1.640000     1    15    17    48    49
    17  C      3.377000   -0.530000    1.475000     1     1    16    50    51
    18  H      4.671000    0.550000    0.116000     5     1
    19  H      3.755000   -0.762000   -0.660000     5     1
    20  H      1.679000    0.579000   -0.660000     5     2
    21  H      3.018000    1.505000   -1.395000     5     2
    22  H      3.381000    2.608000    0.937000     5     3
    23  H      1.815000    1.900000    1.429000     5     3
    24  H      2.347000    3.909000   -0.854000     5     4
    25  H      1.532000    4.239000    0.700000     5     4
    26  H      0.452000    2.493000   -1.620000     5     5
    27  H     -0.086000    4.125000   -1.135000     5     5
    28  H     -0.744000    3.115000    1.172000     5     6
    29  H     -0.431000    1.498000    0.450000     5     6
    30  H     -2.108000    2.086000   -1.416000     5     7
    31  H     -2.417000    3.633000   -0.591000     5     7
    32  H     -4.215000    2.117000   -0.015000     5     8
    33  H     -3.244000    2.434000    1.451000     5     8
    34  H     -3.954000    0.057000    1.293000     5     9
    35  H     -2.175000    0.197000    1.282000     5     9
    36  H     -2.127000   -0.180000   -1.195000     5    10
    37  H     -3.907000   -0.068000   -1.276000     5    10
    38  H     -3.118000   -2.415000   -1.435000     5    11
    39  H     -4.187000   -2.162000   -0.025000     5    11
    40  H     -2.245000   -3.667000    0.466000     5    12
    41  H     -2.288000   -2.235000    1.535000     5    12
    42  H     -0.504000   -1.129000    0.214000     5    13
    43  H     -0.515000   -2.442000   -1.003000     5    13
    44  H      0.349000   -4.067000    0.578000     5    14
    45  H      0.071000   -3.002000    1.990000     5    14
    46  H      1.980000   -2.210000   -0.301000     5    15
    47  H      2.526000   -3.201000    1.089000     5    15
    48  H      1.862000   -1.463000    2.711000     5    16
    49  H      1.204000   -0.419000    1.432000     5    16
    50  H      3.489000    0.276000    2.239000     5    17
    51  H      4.160000   -1.289000    1.717000     5    17
'''

test_in_2 = '''\
    51  19.1064
     1  C      3.825000    0.082000    0.053000     1     2    17    18    19
     2  C      2.983000    1.275000   -0.435000     1     1     3    20    21
     3  C      2.330000    2.062000    0.714000     1     2     4    22    23
     4  C      1.634000    3.354000    0.252000     1     3     5    24    25
     5  C      0.375000    3.157000   -0.610000     1     4     6    26    27
     6  C     -0.771000    2.457000    0.140000     1     5     7    28    29
     7  C     -2.090000    2.484000   -0.650000     1     6     8    30    31
     8  C     -3.299000    1.986000    0.161000     1     7     9    32    33
     9  C     -3.213000    0.528000    0.646000     1     8    10    34    35
    10  C     -3.206000   -0.495000   -0.499000     1     9    11    36    37
    11  C     -3.262000   -1.954000   -0.014000     1    10    12    38    39
    12  C     -2.040000   -2.430000    0.791000     1    11    13    40    41
    13  C     -0.726000   -2.378000   -0.006000     1    12    14    42    43
    14  C      0.437000   -3.056000    0.738000     1    13    15    44    45
    15  C      1.695000   -3.231000   -0.132000     1    14    16    46    47
    16  C      2.364000   -1.926000   -0.598000     1    15    17    48    49
    17  C      3.009000   -1.126000    0.547000     1     1    16    50    51
    18  H      4.498000    0.434000    0.872000     5     1
    19  H      4.499000   -0.256000   -0.770000     5     1
    20  H      2.210000    0.924000   -1.156000     5     2
    21  H      3.651000    1.970000   -0.996000     5     2
    22  H      3.126000    2.342000    1.445000     5     3
    23  H      1.610000    1.420000    1.270000     5     3
    24  H      2.370000    3.975000   -0.313000     5     4
    25  H      1.352000    3.952000    1.152000     5     4
    26  H      0.621000    2.592000   -1.539000     5     5
    27  H      0.024000    4.165000   -0.937000     5     5
    28  H     -0.927000    2.962000    1.122000     5     6
    29  H     -0.484000    1.399000    0.342000     5     6
    30  H     -1.979000    1.896000   -1.590000     5     7
    31  H     -2.299000    3.535000   -0.963000     5     7
    32  H     -4.224000    2.105000   -0.452000     5     8
    33  H     -3.426000    2.651000    1.049000     5     8
    34  H     -4.095000    0.321000    1.299000     5     9
    35  H     -2.313000    0.400000    1.289000     5     9
    36  H     -2.312000   -0.349000   -1.146000     5    10
    37  H     -4.095000   -0.305000   -1.148000     5    10
    38  H     -3.381000   -2.622000   -0.901000     5    11
    39  H     -4.181000   -2.091000    0.605000     5    11
    40  H     -2.228000   -3.484000    1.106000     5    12
    41  H     -1.935000   -1.838000    1.730000     5    12
    42  H     -0.459000   -1.315000   -0.210000     5    13
    43  H     -0.878000   -2.886000   -0.987000     5    13
    44  H      0.107000   -4.070000    1.067000     5    14
    45  H      0.678000   -2.486000    1.665000     5    14
    46  H      1.420000   -3.834000   -1.029000     5    15
    47  H      2.446000   -3.837000    0.430000     5    15
    48  H      1.629000   -1.297000   -1.150000     5    16
    49  H      3.161000   -2.191000   -1.333000     5    16
    50  H      2.234000   -0.790000    1.273000     5    17
    51  H      3.694000   -1.808000    1.104000     5    17
'''

def main():
    unittest.main()

if __name__ == '__main__':
    main()

