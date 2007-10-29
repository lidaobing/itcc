# $Id$
#
# Reference to:
#
# Mihaly Mezei, Efficient Monte Carlo sampling for long molecular
# chains using local moves, tested on a solvated lipid bilayer,
# Journal of Chemical Physics, 2003, 118(8):3874-3879

from math import sqrt, sin, cos, pi
import numpy
from itcc.core import tools
from itcc.ccs2.config import config
from itcc.ccs2.pyramid import pyramid
from itcc.ccs2 import sidechain, rtbis, mezeibase

__revision__ = '$Rev$'
__all__ = ["R6", "r6_base"]


class Mezei(mezeibase.MezeiBase):
    def __init__(self):
        self.min_abs_dist = 1.0

    def _calc_p3(self, points, d13, d35):
        p0 = points[0]
        p1 = points[1]
        p5 = points[2]
        V15 = p5 - p1
        d15 = tools.length(V15)

        if d13 + d35 < d15 or d13 + d15 < d35 or d15 + d35 < d13:
            return None

        c = (d13 * d13 - d35 * d35) / ( 2 * d15 * d15) + 0.5
        r = sqrt(d13 * d13 - c * c * d15 * d15)
        p3o = p1 + c * V15

        Oz = tools.normal(V15)
        p3y = tools.normal(numpy.cross(Oz, p0-p1)) * r
        p3x = numpy.cross(p3y, Oz)
        return (p3o, p3x, p3y)

    def _calc_p2_p4(self, points, len1, len2, p3_result, angle):
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
                return tools.length(self.p2-self.p4) - self.d24
        def switch(self, mode):
            self.mode = mode

    # FIXME: can't find all 6 results of following input:
    #        points = numpy.array(((0.0, 0.0, 0.0),
    #                              (1.0, 0.0, 0.0),
    #                              (2.0, 2.0, 1.0),
    #                              (2.0, 2.0, 2.0)))
    #        len1 = numpy.array((1.0, 1.0, 1.0, 1.0))
    #        len2 = numpy.array((math.sqrt(2.0),)*5)
    def r6_base(self, points, len1, len2, error=0.1):
        """r6_base(points, len1, len2) -> iterator

        len(points) == 4
        len(len1) == 4
        len(len2) == 5

        return all results fulfill following conditions in a iterator,
        len(result) will be 3.

        distance(points[1], result[0]) = len1[0];
        distance(result[0], result[1]) = len1[1];
        distance(result[1], result[2]) = len1[2];
        distance(result[2], points[2]) = len1[3];
        distance(points[0], result[0]) = len2[0];
        distance(points[1], result[1]) = len2[1];
        distance(result[0], result[2]) = len2[2];
        distance(result[1], points[2]) = len2[3];
        distance(result[2], points[3]) = len2[4];
        """

        assert(len(points) == 4 and
               len(len1) == 4 and
               len(len2) == 5)
        p0, p1, p5, p6 = tuple(points)
        d12, d23, d34, d45 = tuple(len1)
        d02, d13, d24, d35, d46 = tuple(len2)

        p3_result = self._calc_p3((p0, p1, p5), d13, d35)
        if p3_result is None:
            return
        p3o, p3x, p3y = p3_result

        steps = config.get('Mezei_R6_steps', 36)
        step = 2 * pi / steps

        d24s = numpy.zeros((4, steps+1), float)
        for i in range(steps):
            angle = i * step
            p24_result = self._calc_p2_p4(points, len1, len2, p3_result, angle)
            if p24_result:
                p2s, p4s = p24_result
                d24s[0][i] = tools.length(p2s[0] - p4s[0])
                d24s[1][i] = tools.length(p2s[0] - p4s[1])
                d24s[2][i] = tools.length(p2s[1] - p4s[0])
                d24s[3][i] = tools.length(p2s[1] - p4s[1])
        d24s[0][steps] = d24s[0][0]
        d24s[1][steps] = d24s[1][0]
        d24s[2][steps] = d24s[2][0]
        d24s[3][steps] = d24s[3][0]

        p24_res = self.p24_Resolver(points, len1, len2, p3_result)
        for i in range(4):
            p24_res.switch(i)
            for j in range(steps):
                if d24s[i][j] and d24s[i][j+1] and \
                       (d24s[i][j] - d24)*(d24s[i][j+1] - d24) <= 0:
                    try:
                        angle = rtbis.rtbis(p24_res, j*step, (j+1)*step, error)
                        yield (i, angle, p24_res.p2, p24_res.p3, p24_res.p4)
                    except rtbis.Error:
                        pass

    def __R6(self, coords, atmidx, dismat):
        assert len(atmidx) == 7
        points = [coords[atmidx[i]] for i in (0, 1, 5, 6)]
        len1idx = ((1, 2), (2, 3), (3, 4), (4, 5))
        len1 = [dismat[atmidx[i], atmidx[j]] for i, j in len1idx]
        len2idx = ((0, 2), (1, 3), (2, 4), (3, 5), (4, 6))
        len2 = [dismat[atmidx[i], atmidx[j]] for i, j in len2idx]
        for _result in r6_base(points, len1, len2):
            result = {}
            result[atmidx[2]] = _result[2]
            result[atmidx[3]] = _result[3]
            result[atmidx[4]] = _result[4]
            yield result

    def R6(self, coords, atmidx, dismat, shakedata):
        '''Wrapped R6 algorithm, include R6 and shakeH'''
        shakes = [shakedata[idx] for idx in atmidx[1:-1]]
        for baseresult in self.__R6(coords, atmidx, dismat):
            newcoords = coords.copy()
            abs_dist = 0.0 
            for idx, newcoord in baseresult.items():
                newcoords[idx] = newcoord
                abs_dist += sum(abs(newcoord - coords[idx]))
            if abs_dist < self.min_abs_dist:
                continue
            for refidxs, sidechain_ in shakes:
                baseresult.update(sidechain.movesidechain(coords, newcoords, refidxs, sidechain_))
            yield baseresult

_inst = Mezei()
R6 = _inst.R6
r6_base = _inst.r6_base

