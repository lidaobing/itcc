# $Id$
#
# Reference to:
#
# Mihaly Mezei, Efficient Monte Carlo sampling for long molecular
# chains using local moves, tested on a solvated lipid bilayer,
# Journal of Chemical Physics, 2003, 118(8):3874-3879

from math import sqrt, sin, cos, pi
import Numeric
from itcc.CCS2.config import config
from itcc.CCS2.pyramid import pyramid

__revision__ = '$Rev$'
__all__ = ["R6"]

def rtbis(func, x1, x2, xacc):
    "Reference: Numerical Recipes in C, Chapter 9.1, Page 354"
    f = func(x1)
    fmid = func(x2)
    if f * fmid >= 0:
        raise RuntimeError

    if f < 0.0:
        dx = x2 - x1
        rtb = x1
    else:
        dx = x1 - x2
        rtb = x2

    while True:
        dx *= 0.5
        xmid = rtb + dx
        fmid = func(xmid)
        if fmid <= 0.0:
            rtb = xmid
        if abs(dx) < xacc or fmid == 0.0:
            return rtb
    return None                         # never get here

def _calc_p3(points, d13, d35):
    p0 = points[0]
    p1 = points[1]
    p5 = points[2]
    V15 = p5 - p1
    d15 = V15.length()
    
    if d13 + d35 < d15 or d13 + d15 < d35 or d15 + d35 < d13:
        return None

    c = (d13 * d13 - d35 * d35) / ( 2 * d15 * d15) + 0.5
    r = sqrt(d13 * d13 - c * c * d15 * d15)
    p3o = p1 + c * V15

    Oz = V15.normal()
    p3y = Oz.cross(p0-p1).normal() * r
    p3x = p3y.cross(Oz)
    return (p3o, p3x, p3y)

def _calc_p2_p4(points, len1, len2, p3_result, angle):
    p0, p1, p5, p6 = tuple(points)
    d12, d23, d34, d45 = tuple(len1)
    d02, d13, d24, d35, d46 = tuple(len2)
    
    threshold = config.get('Mezei_p24_threshold', -0.01*0.01)
    
    p3o, p3x, p3y = p3_result
    p3 = p3o + p3x * cos(angle) + p3y * sin(angle)
    p2s, z2s = pyramid(p0, p1, p3, d02, d12, d23)
    if z2s < threshold:
        return None
    p4s, z4s = pyramid(p6, p5, p3, d46, d45, d34)
    if z4s < threshold:
        return None
    return (p2s, p4s)

class p24_Resolver:
    def __init__(self, points, len1, len2, p3_result):
        self.p0, self.p1, self.p5, self.p6 = tuple(points)
        self.d12, self.d23, self.d34, self.d45 = tuple(len1)
        self.d02, self.d13, self.d24, self.d35, self.d46 = tuple(len2)
        self.p3o, self.p3x, self.p3y = p3_result
        self.threshold = config.get('Mezei_p24_threshold', -0.01*0.01)
        self.mode = -1
    def __call__(self, angle):
        self.p3 = self.p3o + self.p3x * cos(angle) + self.p3y * sin(angle)
        p2s, z2s = pyramid(self.p0, self.p1, self.p3, self.d02,
                           self.d12, self.d23) 
        if z2s < self.threshold:
            return None
        p4s, z4s = pyramid(self.p6, self.p5, self.p3, self.d46,
                           self.d45, self.d34) 
        if z4s < self.threshold:
            return None
        if self.mode == -1:
            return (p2s, p4s)
        else:
            i2 = self.mode / 2
            i4 = self.mode % 2
            self.p2 = p2s[i2]
            self.p4 = p4s[i4]
            return (self.p2-self.p4).length() - self.d24
    def switch(self, mode):
        self.mode = mode

def R6(points, len1, len2):
    assert(len(points) == 4 and
           len(len1) == 4 and
           len(len2) == 5)
    p0,p1,p5,p6 = tuple(points)
    d12,d23,d34,d45 = tuple(len1)
    d02,d13,d24,d35,d46 = tuple(len2)

    p3_result = _calc_p3((p0,p1,p5), d13, d35)
    if p3_result is None:
        return []
    p3o, p3x, p3y = p3_result
    
    steps = config.get('Mezei_R6_steps', 36)
    step = 2 * pi / steps
    
    d24s = Numeric.zeros((4, steps+1), Numeric.Float)
    for i in range(steps):
        angle = i * step
        p24_result = _calc_p2_p4(points, len1, len2, p3_result, angle)
        if p24_result:
            p2s, p4s = p24_result
            d24s[0][i] = (p2s[0] - p4s[0]).length()
            d24s[1][i] = (p2s[0] - p4s[1]).length()
            d24s[2][i] = (p2s[1] - p4s[0]).length()
            d24s[3][i] = (p2s[1] - p4s[1]).length()
    d24s[0][steps] = d24s[0][0]
    d24s[1][steps] = d24s[1][0]
    d24s[2][steps] = d24s[2][0]
    d24s[3][steps] = d24s[3][0]

    result = []
    p24_res = p24_Resolver(points, len1, len2, p3_result)
    for i in range(4):
        p24_res.switch(i)
        for j in range(steps):
            if d24s[i][j] and d24s[i][j+1] and \
                   (d24s[i][j] - d24)*(d24s[i][j+1] - d24) <= 0: 
                angle = rtbis(p24_res, j*step, (j+1)*step, 0.1)
                result.append((i, angle, p24_res.p2, p24_res.p3, p24_res.p4))
    return result
        

if __name__ == '__main__':
    from Scientific.Geometry import Vector
    p0 = Vector(0.0, 0.0, 1.0)
    p1 = Vector(0.0, 0.0, 0.0)
    p5 = Vector(1.0, 0.0, 0.0)
    print _calc_p3([p0, p1, p5], 1.4, 1.4)
