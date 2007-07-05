# $Id$
# -*- coding: utf-8 -*-
"""extend Mezei's method to protein.
"""
import math
from itcc.core import tools
from itcc.ccs2 import pyramid, sidechain
from itcc.ccs2 import config, rtbis

__revision__ = '$Rev$'

def _wrappyramid(atmidx, coords, dismat):
    '''_wrappyramid((i1, i2, i3, i4), coords, dismat)

    coords是坐标，dismat是距离矩阵，已知i2, i3, i4三个点的坐标，求i1的坐标。

    一般情况下i1有两个解(r1, r2), 这时返回 (r1, r2)，
    如果没有解，返回 (None, None)

    浮点数误差部分参见 config.Mezei_p24_threshold
    '''
    i1, i2, i3, i4 = atmidx
    A = coords[i2]
    B = coords[i3]
    C = coords[i4]
    rAX = dismat[i1, i2]
    rBX = dismat[i1, i3]
    rCX = dismat[i1, i4]
    results, error = pyramid.pyramid(A, B, C, rAX, rBX, rCX)
    threshold = config.config.get('Mezei_p24_threshold', -0.01*0.01)
    if error < threshold:
        yield None
        yield None
    else:
        yield results[0]
        yield results[1]

def wrappyramid2(atmidx, coords, dismat):
    i1, i2, i3 = atmidx
    A = coords[i2]
    B = coords[i3]
    rAX = dismat[i1, i2]
    rBX = dismat[i1, i3]
    return pyramid.pyramid2(A, B, rAX, rBX)

def propyramida(atmidx, coords, dismat):
    '''resolve a fragment of protein:
    C1-C2(=O)-N3-C4-C5(=O) or
    N5-C4-C3(=O)-N2-C1

    known the coords of p1, p4, p5, and all the bond length and bond
    length and bond angles, to calculate the coords of p2 and p3
    '''
    i1, i2, i3, i4, i5 = tuple(atmidx)
    for i3coord in _wrappyramid((i3, i1, i4, i5), coords, dismat):
        if i3coord is None:
            yield (None, None)
            yield (None, None)
            continue
        newcoords = coords.copy()
        newcoords[i3] = i3coord
        i2coords = tuple(_wrappyramid((i2, i1, i3, i4), 
                                      newcoords, dismat))
        if i2coords[0] is None:
            yield (None, None)
            yield (None, None)
            continue
        yield (i2coords[0], i3coord)
        yield (i2coords[1], i3coord)

def safeop(op, *args):
    for arg in args:
        if arg is None:
            return None
    return op(*args)

class R6sub:
    def __init__(self, coords, atmidx, dismat):
        assert len(atmidx) == 9, atmidx
        self.coords = coords
        self.atmidx = atmidx
        self.dismat = dismat
        i1, i2, i3, i4, i5, i6, i7, i8, i9 = atmidx
        self.p5o, self.p5x, self.p5y = wrappyramid2((i5, i2, i8),
                                                    coords, dismat)
    def __call__(self, angle):
        i1, i2, i3, i4, i5, i6, i7, i8, i9 = self.atmidx
        p5 = self.p5o + self.p5x * math.cos(angle) + self.p5y * math.sin(angle)
        newcoords = self.coords.copy()
        newcoords[i5] = p5
        resultsa = propyramida((i5, i4, i3, i2, i1),
                               newcoords, self.dismat)
        resultsb = tuple(propyramida((i5, i6, i7, i8, i9),
                                     newcoords, self.dismat))

        for p4, p3 in resultsa:
            for p6, p7 in resultsb:
                if p4 is None or p6 is None:
                    yield (None,) * 5
                else:
                    yield (p3, p4, p5, p6, p7)

def R6a(coords, atmidx, dismat):
    '''resolve a fragment of protein:
    N1-C2-C3(=O)-N4-C5-C6(=O)-N7-C8-C9(=O)

    known the coords of p1, p2, p8, p9, and all the bond length and
    bond length and bond angles, to calculate the coords from p3 to p7
    '''
    r6sub = R6sub(coords, atmidx, dismat)
    i1, i2, i3, i4, i5, i6, i7, i8, i9 = atmidx

    steps = config.config.get('Mezei_R6_steps', 36)
    stepsize = 2 * math.pi / steps

    results = [r6sub(i*stepsize) for i in range(steps)]
    results[0] = tuple(results[0])
    results.append(results[0])

    d46ref = dismat[i4, i6]
    d46mat = [[getd46rela(ps[1], ps[3], d46ref) for ps in result]
              for result in results]

    results = []
    for i in range(steps):
        for j in range(16):
            if d46mat[i][j] is not None \
              and d46mat[i+1][j] is not None \
              and d46mat[i][j] * d46mat[i+1][j] <= 0:
                try:
                    angle = rtbis.rtbis(d46_Resolver(r6sub, j, d46ref),
                                  i * stepsize,
                                  (i+1) * stepsize,
                                  math.radians(1.0))
                    result = tuple(r6sub(angle))[j]
                    yield {i3: result[0],
                           i4: result[1],
                           i5: result[2],
                           i6: result[3],
                           i7: result[4]}
                except rtbis.Error:
                    pass

def getd46rela(p4, p6, d46ref):
    if p4 is None or p6 is None:
        return None
    return tools.length(p4 - p6) - d46ref

class d46_Resolver:
    def __init__(self, r6sub, mode, d46ref):
        self.r6sub = r6sub
        self.d46ref = d46ref
        self.mode = mode
    def __call__(self, angle):
        result = tuple(self.r6sub(angle))[self.mode]
        if result[1] is None: return None
        return tools.length(result[1] - result[3]) - self.d46ref


def R6(coords, atmidx, dismat, shakedata):
    '''Wrapped R6 algorithm, include R6 and shakeH'''
    shakes = [shakedata[idx] for idx in atmidx[1:-1]]
    for baseresult in R6a(coords, atmidx, dismat):
        newcoords = coords.copy()
        for idx, newcoord in baseresult.items():
            newcoords[idx] = newcoord
        for refidxs, sidechain_ in shakes:
            baseresult.update(sidechain.movesidechain(coords, newcoords,
                                                      refidxs, sidechain_))
        yield baseresult
