# $Id$
from math import sqrt, sin, cos, pi
from Scientific.Geometry import Vector
from itcc.Tools import ctools
from itcc.Tools import cpptools

__revision__ = '$Rev$'
__all__ = ['length', 'angle', 'torsionangle', 'imptor', 'shakeH2',
           'combinecombine', 'xyzatm', 'minidx', 'maxidx',
           'weightedmean', 'weightedsd']

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
    angle = ad.angle(abc)
    return pi - angle

def shakeH2(p0, p1, p2, CHlen=1.113):
    p3, p4 = cpptools.shakeH2(tuple(p0.array), tuple(p1.array),
                              tuple(p2.array), CHlen) 
    p3 = Vector(p3)
    p4 = Vector(p4)
    return p3, p4

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

if __name__ == '__main__':
    a_ = Vector(0, 0, 0)
    b_ = Vector(1.0, 0.0, 0.0)
    c_ = Vector(1.0, 1.0, 0.0)
    d_ = Vector(1.0, 1.0, 1.0)
    print torsionangle(a_, b_, c_, d_)

    print

    
    p0_ = Vector(0, 0, 0)
    p1_ = Vector(0, 0, 1.089)
    p2_ = Vector(1.026719,    0.000000,   -0.363000)
    print shakeH2(p0_, p1_, p2_, 1.089)

    p0_ = Vector(0, 0, 0)
    p1_ = Vector(-1, 1, 1)
    p2_ = Vector(-1, -1, -1)
    print shakeH2(p0_, p1_, p2_, 1.732)

    
    
    
#      5 molden generated tinker .xyz (mm3 param.)
#     1  C     0.000000    0.000000    0.000000      1     2    3    4    5
#     2  H     0.000000    0.000000    1.089000      5     1
#     3  H     1.026719    0.000000   -0.363000      5     1
#     4  H    -0.513360   -0.889165   -0.363000      5     1
#     5  H    -0.513360    0.889165   -0.363000      5     1

    
