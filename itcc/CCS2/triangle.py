# $Id$

"""some triangle functions

given a triangle OAB, calculate some reuslt from some given.

angle's unit is radian not degree.

if failed, return None
"""

import math

def calc_ab(oa, ob, aob):
    """calc_ab(oa, ob, aob) -> float
    given OA, OB and angle AOB, calculate AB
    angle's unit is radian not degree.

    for example:
    >>> calc_ab(3,4,math.radians(90)) == 5
    True
    """
    return math.sqrt(oa*oa + ob*ob - 2*oa*ob*math.cos(aob))

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
