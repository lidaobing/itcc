# $Id$
import sys
import random
import math
import numpy
from itcc.core import ctools

__revision__ = '$Rev$'
__all__ = ['length', 'angle', 'torsionangle', 'imptor',
           'combinecombine', 'xyzatm', 'minidx', 'maxidx',
           'weightedmean', 'weightedsd', 'datafreq',
           'random_vector', 'all', 'any',
           'dissq', 'lensq', 'distance', 'normal']

def normal(a):
    return a / length(a)

def datafreq(data, min_, max_, num):
    result = [0] * num
    step = float(max_ - min_)/num

    for x in data:
        type_ = int((x - min_)/step)
        if 0 <= type_ < num:
            result[type_] += 1

    return result

def distance(a, b):
    return length(a-b)

def dissq(a, b):
    return lensq(a-b)

def length(a):
    return math.sqrt(sum(a*a))

def lensq(a):
    return sum(a*a)

def angle(a, b, c):
    return ctools.angle(tuple(a), tuple(b), tuple(c))

def torsionangle(a, b, c, d):
    """torsionangle(a, b, c, d) -> angle
    a, b, c, d are 4 numpy.array
    return the torsionangle of a-b-c-d in radian, range is (-pi, pi].
    if torsionangle is invalid, for example, a == b or b == c or c == d
    or a == c or b == d, then return float("nan").
    """

    return ctools.torsionangle(tuple(a), tuple(b),
                               tuple(c), tuple(d))

def imptor(a, b, c, d):
    '''imptor(a, b, c, d) -> angle
    a, b, c, d are 4 Scientific.Geometry.Vector
    return the imptor of a-b-c-d

    imptor(abcd) is the angle between vector ad and plane abc,
    crossmulti(ab, ac) is the positive direction.
    '''
    ad = d - a
    ab = b - a
    ac = c - a
    abc = numpy.cross(ab, ac)
    angle_ = ad.angle(abc)
    return math.pi - angle_

def combinecombine(cmbs):
    if not cmbs:
        yield []
        return
    for x in cmbs[0]:
        for cc in combinecombine(cmbs[1:]):
            yield [x] + cc

def xyzatm(p1, p2, p3, r, theta, phi):
    '''
    >>> from Scientific.Geometry import Vector
    >>> import math
    >>> xyzatm(Vector(0,0,1), Vector(0,0,0), Vector(1,0,0),
    ...        1, math.radians(90), 0)
    Vector(1.0,0.0,0.99999999999999989)
    '''

    r12 = normal(p1 - p2)
    r23 = normal(p2 - p3)
    rt = numpy.cross(r23, r12)
    cosine = r12 * r23
    sine = math.sqrt(max(1.0 - cosine*cosine, 0.0))
    rt /= sine
    ru = numpy.cross(rt, r12)
    ts = math.sin(theta)
    tc = math.cos(theta)
    ps = math.sin(phi)
    pc = math.cos(phi)
    return p1 + (ru * (ts * pc) + rt * (ts * ps) - r12 * tc) * r

def minidx(iterable):
    iterable = iter(iterable)
    idx = 0
    item = iterable.next()
    for i, x in enumerate(iterable):
        if x < item:
            idx = i+1
            item = x
    return idx, item

def maxidx(iterable):
    iterable = iter(iterable)
    idx = 0
    item = iterable.next()
    for i, x in enumerate(iterable):
        if x > item:
            idx = i+1
            item = x
    return idx, item

def swapaxes(matrix):
    rank1 = len(matrix)
    if rank1 == 0:
        return []
    rank2 = len(matrix[0])
    for row in matrix:
        assert len(row) == rank2

    result = [[None] * rank1 for i in range(rank2)]

    for i in range(rank2):
        for j in range(rank1):
            result[i][j] = matrix[j][i]

    return result

def weightedmean(datas, weights):
    assert len(datas) == len(weights)
    sum_ = sum([data * weight for data, weight in zip(datas, weights)])
    totalweight = sum(weights)
    return sum_/totalweight

def weightedsd(datas, weights):
    assert len(datas) == len(weights)
    assert len(datas) > 1
    mean_ = weightedmean(datas, weights)
    sum_ = sum([(data - mean_)**2 * weight \
                for data, weight in zip(datas, weights)])
    totalweight = sum(weights)
    return math.sqrt(sum_/totalweight)

def any(iterable):
    for element in iterable:
        if element:
            return True
    return False

def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True

def random_vector(length_=1.0):
    z = random.uniform(-length_, length_)
    s = math.sqrt(length_*length_ - z*z)
    theta = random.uniform(0.0, math.pi*2)
    x = s * math.cos(theta)
    y = s * math.sin(theta)
    return (x, y, z)

def open_file_or_stdin(ifname):
    if ifname == '-':
        return sys.stdin
    else:
        return file(ifname)

def sorted_(iterable):
    '''python 2.3 does not support sorted'''
    res = list(iterable)
    res.sort()
    return res

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
