# $Id$
import random
from math import sqrt, sin, cos, pi
from Scientific.Geometry import Vector
from itcc.Tools import ctools

__revision__ = '$Rev$'
__all__ = ['length', 'angle', 'torsionangle', 'imptor',
           'combinecombine', 'xyzatm', 'minidx', 'maxidx',
           'weightedmean', 'weightedsd', 'datafreq', 'any', 'all',
           'random_vector']

def datafreq(data, min_, max_, num):
    result = [0] * num
    step = float(max_ - min_)/num

    for x in data:
        type_ = int((x - min_)/step)
        if 0 <= type_ < num:
            result[type_] += 1

    return result

def length(a, b):
    return (a-b).length()

def angle(a, b, c):
    return (a-b).angle(c-b)

def torsionangle(a, b, c, d):
    """torsionangle(a, b, c, d) -> angle
    a, b, c, d are 4 Scientific.Geometry.Vector
    return the torsionangle of a-b-c-d"""

    return ctools.torsionangle(tuple(a.array), tuple(b.array),
                               tuple(c.array), tuple(d.array))

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
    abc = ab.cross(ac)
    angle_ = ad.angle(abc)
    return pi - angle_

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
    r12 = (p1 - p2).normal()
    r23 = (p2 - p3).normal()
    rt = r23.cross(r12)
    cosine = r12 * r23
    sine = sqrt(max(1.0 - cosine*cosine, 0.0))
    rt /= sine
    ru = rt.cross(r12)
    ts = sin(theta)
    tc = cos(theta)
    ps = sin(phi)
    pc = cos(phi)
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
    mean = weightedmean(datas, weights)
    sum_ = sum([(data - mean)**2 * weight \
                for data, weight in zip(datas, weights)])
    totalweight = sum(weights)
    return sqrt(sum_/totalweight)

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
    s = sqrt(length_*length_ - z*z)
    theta = random.uniform(0.0, pi+pi)
    x = s * cos(theta)
    y = s * sin(theta)
    return (x, y, z)

if __name__ == '__main__':
    a_ = Vector(0, 0, 0)
    b_ = Vector(1.0, 0.0, 0.0)
    c_ = Vector(1.0, 1.0, 0.0)
    d_ = Vector(1.0, 1.0, 1.0)
    print torsionangle(a_, b_, c_, d_)
