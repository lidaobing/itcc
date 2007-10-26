# $Id$

'''

C0-C1-N2-C3-C4-N5-C6-C7-N8-C9
   ||       ||       ||
   O        O        O

Problem:

known all bond length and bond angles, fix torsion angle between C(=O)
and N, known coordinates of C0, C1, N8, C9, calculate all other
coordinates.


Solution:

detect circle of N2
for each N2 on the circle of N2
  calculate C3 from p0, p1, p2
  calculate C6 from p3, p8, p9 (dupe)
  calculate C4 from p2, p3, p6 (dupe)
  calculate N5 from p3, p4, p6 (dupe)
  calculate C7 from p6, p8, p9 (dupe)
'''

import math
from itcc.ccs2 import pyramid, sidechain, rtbis
from itcc.core import tools

class Error(Exception):
    pass

class Mezeipro2:
    def __init__(self, coords, dismatrix, idxs):
        self.coords = coords
        self.dismatrix = dismatrix
        self.idxs = idxs
        assert len(self.idxs) == 10
        self.steps = 36
        self.threshold = -0.01 * 0.01
        self.acc = math.radians(0.1)

        p0 = self._coord(0)
        p1 = self._coord(1)
        r02 = self._dismatrix(0, 2)
        r12 = self._dismatrix(1, 2)
        self.p2o, self.p2x, self.p2y = pyramid.pyramid2(p0, p1, r02, r12)

        if self.p2o is None:
            raise Error()

    def __call__(self):
        result = [[] for i in range(16)]

        stepsize = math.pi * 2 / self.steps
        ref = self._dismatrix(5, 7)
        for i in range(self.steps):
            p2 = self.p2o \
                 + self.p2x * math.cos(stepsize * i) \
                 + self.p2y * math.sin(stepsize * i)
            tmps = list(self.get_p34567(p2))
            assert len(tmps) == 16
            for idx, tmp in enumerate(tmps):
                if tmp[0] is None:
                    result[idx].append(None)
                else:
                    result[idx].append(tools.length(tmp[2] - tmp[4]) - ref)

        for i in range(16):
            result[i].append(result[i][0])

        for i in range(16):
            def _Func(x):
                try:
                    return tuple(self.get_r57_from_theta(x))[i] - ref
                except TypeError:
                    return None
            func = _Func
            for j in range(self.steps):
                if result[i][j] is None: continue
                if result[i][j+1] is None: continue
                if result[i][j] * result[i][j+1] > 0: continue
                try:
                    tmp = rtbis.rtbis(func, j*stepsize, (j+1)*stepsize, self.acc)
                    p2 = self._theta_to_p2(tmp)
                    tmp2 = self.get_p34567(p2)
                    for _k in range(i+1):
                        tmp3 = tmp2.next()
                    yield tuple([p2,] + list(tmp3))
                except rtbis.Error:
                    pass

    def _theta_to_p2(self, theta):
        return self.p2o \
                 + self.p2x * math.cos(theta) \
                 + self.p2y * math.sin(theta)

    def _coord(self, idx):
        return self.coords[self.idxs[idx]]

    def _dismatrix(self, i1, i2):
        return self.dismatrix[self.idxs[i1], self.idxs[i2]]

    def get_r57_from_theta(self, theta):
        p2 = self._theta_to_p2(theta)
        for p3, p4, p5, p6, p7 in self.get_p34567(p2):
            if p3 is None:
                yield None
            else:
                yield tools.length(p5 - p7)

    def get_p34567(self, p2):
        for p3 in self.get_p3(p2):
            if p3 is None:
                for _i in range(16):
                    yield (None,) * 5
                continue
            for p6 in self.get_p6(p3):
                if p6 is None:
                    for _i in range(8):
                        yield (None,) * 5
                    continue
                for p4 in self.get_p4(p2, p3, p6):
                    if p4 is None:
                        for _i in range(4):
                            yield (None,) * 5
                        continue
                    for p5 in self.get_p5(p3, p4, p6):
                        if p5 is None:
                            for _i in range(2):
                                yield (None,) * 5
                            continue
                        for p7 in self.get_p7(p6):
                            if p7 is None:
                                yield (None,) * 5
                            else:
                                yield p3, p4, p5, p6, p7

    def get_p2(self):
        n2o, n2x, n2y = self.p2o, self.p2x, self.p2y
        if n2o is None:
            return

        steps = self.steps
        stepsize = 2 * math.pi / steps

        for i in range(steps):
            yield n2o + n2x * math.cos(stepsize * i) + n2y * math.sin(stepsize * i)

    def get_p3(self, p2):
        results, error = pyramid.pyramid(self._coord(0),
                                         self._coord(1),
                                         p2,
                                         self._dismatrix(0, 3),
                                         self._dismatrix(1, 3),
                                         self._dismatrix(2, 3))
        if error >= self.threshold:
            yield (results[0] + results[1]) / 2.0
        else:
            yield None

    def get_p6(self, p3):
        results, error = pyramid.pyramid(p3,
                                         self._coord(8),
                                         self._coord(9),
                                         self._dismatrix(6, 3),
                                         self._dismatrix(6, 8),
                                         self._dismatrix(6, 9))
        if error >= self.threshold:
            for result in results:
                yield result
        else:
            yield None
            yield None

    def get_p4(self, p2, p3, p6):
        results, error = pyramid.pyramid(p2, p3, p6,
                                         self._dismatrix(4, 2),
                                         self._dismatrix(4, 3),
                                         self._dismatrix(4, 6))
        if error >= self.threshold:
            for result in results:
                yield result
        else:
            yield None
            yield None

    def get_p5(self, p3, p4, p6):
        results, error = pyramid.pyramid(p3, p4, p6,
                                         self._dismatrix(5, 3),
                                         self._dismatrix(5, 4),
                                         self._dismatrix(5, 6))
        if error >= self.threshold:
            yield results[0]
            yield results[1]
        else:
            yield None
            yield None

    def get_p7(self, p6):
        results, error = pyramid.pyramid(p6,
                                         self._coord(8),
                                         self._coord(9),
                                         self._dismatrix(7, 6),
                                         self._dismatrix(7, 8),
                                         self._dismatrix(7, 9))
        if error >= self.threshold:
            yield results[0]
            yield results[1]
        else:
            yield None
            yield None

def _print_result(ofile, result):
    for coord in result:
        if coord is not None:
            ofile.write('%10.6f %10.6f %10.6f\n' % tuple(coord))
        else:
            ofile.write(str(None) + '\n')

def R6(coords, atmidx, dismat, shakedata):
    '''Wrapped R6 algorithm, include R6 and shakeH'''
    shakes = [shakedata[idx] for idx in atmidx[1:-1]]
    mezeipro2 = Mezeipro2(coords, dismat, atmidx)
    for result in mezeipro2():
        baseresult = {}
        for i in range(2,8):
            baseresult[atmidx[i]] = result[i-2]
        newcoords = coords.copy()
        for idx, newcoord in baseresult.items():
            newcoords[idx] = newcoord
        for refidxs, sidechain_ in shakes:
            baseresult.update(sidechain.movesidechain(coords, newcoords,
                                                      refidxs, sidechain_))
        yield baseresult

def _test():
    mol = '''    17  molden generated tinker .xyz (mm3 param.)
     1  N+     0.000000    0.000000    0.000000    39     2
     2  C      0.000000    0.000000    1.460000     1     1     3
     3  C      1.403962    0.000000    2.015868     3     2     4     5
     4  N      2.195124   -0.904100    1.422348     9     3     6
     5  O      1.755111    0.752517    2.909631     7     3
     6  C      3.591293   -1.058240    1.820536     1     4     7
     7  C      4.358438    0.233498    1.668879     3     6     8     9
     8  N      4.140177    0.829026    0.488494     9     7    10
     9  O      5.091799    0.666773    2.542294     7     7
    10  C      4.792149    2.091022    0.151005     1     8    11
    11  C      4.466440    3.170859    1.154979     3    10    12    13
    12  N      3.158394    3.235806    1.438521     9    11    14
    13  O      5.320944    3.893369    1.640987     7    11
    14  C      2.642777    4.216977    2.388806     1    12    15
    15  C      3.289555    4.070161    3.745355     3    14    16    17
    16  O      3.401864    2.975815    4.272794    47    15
    17  O      3.724636    5.023075    4.370703    47    15
    '''

    import StringIO
    mol = StringIO.StringIO(mol)
    from itcc.molecule import read
    mol = read.readxyz(mol)

    from itcc.molecule import tools
    distmat = tools.distmat(mol)

    idxs = [2,3,4,6,7,8,10,11,12,14]
    idxs = [x - 1 for x in idxs]

    import sys
    for x in idxs[2:-2]:
        sys.stdout.write('%10.6f %10.6f %10.6f\n' % tuple(mol.coords[x]))

    mezeipro2 = Mezeipro2(mol.coords, distmat, idxs)

    results = list(mezeipro2())
    print len(results)
    for result in results:
        _print_result(sys.stdout, result)
        if result[3] is not None:
            print tools.length(result[3]-result[5]), mezeipro2._dismatrix(5, 7)

if __name__ == '__main__':
    _test()
