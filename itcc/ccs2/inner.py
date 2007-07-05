# $Id$

"""some functions for inner coordinates

angle and torsion angle's unit is radian.
"""

import math
from itcc.core.tools import xyzatm

def _all(lst):
    for x in lst:
        if not x: return False
    return True

def _calc_3rd(refs, idx1, idx2, radius, theta):
    assert idx1 < len(refs)
    assert idx2 < len(refs)
    assert idx1 != idx2
    assert refs[idx1][2] == refs[idx2][2]

    new_theta = theta + \
                math.atan2(refs[idx2][1] - refs[idx1][1],
                           refs[idx2][0] - refs[idx1][0])
    return (refs[idx1][0] + radius * math.cos(new_theta),
            refs[idx1][1] + radius * math.sin(new_theta),
            refs[idx1][2])

def inner2xyz(inner):
    """inner2xyz(inner) -> xyz coordinate

    >>> xxx = inner2xyz(((-1, -1, -1, -1.0, -1.0, -1.0),
    ...                  ( 0, -1, -1, 1.0, -1.0, -1.0),
    ...                  ( 1,  0, -1, 1.0, math.radians(90.0), -1.0),
    ...                  ( 2,  1,  0,
    ...                    1.0, math.radians(90.0), math.radians(90.0))))
    ...
    >>> print [[round(x, 2) for x in xx] for xx in xxx]
    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, -1.0, 0.0], [1.0, -1.0, -1.0]]
    """
    result = []
    for idx, data in enumerate(inner):
        assert len(data) == 6
        if idx == 0:
            result.append((0.0, 0.0, 0.0))
        elif idx == 1:
            assert data[0] == 0
            result.append((data[3], 0.0, 0.0))
        elif idx == 2:
            result.append(_calc_3rd(result, data[0], data[1], data[3], data[4]))
        else:
            result.append(tuple(xyzatm(result[data[0]],
                                       result[data[1]],
                                       result[data[2]],
                                       data[3],
                                       data[4],
                                       data[5])))
    return result

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
