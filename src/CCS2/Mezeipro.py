# $Id$
"""extend Mezei's method to protein.
"""
import math
import sys
import operator
import Numeric
from Scientific import Geometry
from itcc.CCS2 import pyramid, sidechain
from itcc.CCS2 import config
from itcc.CCS2.Mezei import rtbis

__revision__ = '$Rev$'

def wrappyramid(atmidx, coords, dismat):
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
        return (None, None)
    else:
        return results

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
    N5-C4-C3(-O)-N2-C1

    known the coords of p1, p4, p5, and all the bond length and bond
    length and bond angles, to calculate the coords of p2 and p3
    '''
    i1, i2, i3, i4, i5 = tuple(atmidx)
    result = []
    for i3coord in wrappyramid((i3, i1, i4, i5), coords, dismat):
        if i3coord is None:
            result.append((None, None))
            result.append((None, None))
            continue
        newcoords = coords[:]
        newcoords[i3] = i3coord
        i2coords = wrappyramid((i2, i1, i3, i4), newcoords, dismat)
        if i2coords[0] is None:
            result.append((None, None))
            result.append((None, None))
            continue
        result.append((i2coords[0], i3coord))
        result.append((i2coords[1], i3coord))
    return result

def safeop(op, *args):
    for arg in args:
        if arg is None:
            return None
    return op(*args)

class R6sub:
    def __init__(self, coords, atmidx, dismat):
        self.coords = coords
        self.atmidx = atmidx
        self.dismat = dismat
        i1, i2, i3, i4, i5, i6, i7, i8, i9 = atmidx
        self.p5o, self.p5x, self.p5y = wrappyramid2((i5, i2, i8), coords, dismat)
    def __call__(self, angle):
        i1, i2, i3, i4, i5, i6, i7, i8, i9 = self.atmidx
        p5 = self.p5o + self.p5x * math.cos(angle) + self.p5y * math.sin(angle)
        newcoords = self.coords[:]
        newcoords[i5] = p5
        results = []
        for p4, p3 in propyramida((i5, i4, i3, i2, i1), newcoords, self.dismat):
            if p4 is None:
                results.append((None,)*5)
                results.append((None,)*5)
                continue
            for p6, p7 in propyramida((i5, i6, i7, i8, i9), newcoords, self.dismat):
                if p6 is None:
                    results.append((None,)*5)
                    continue
                results.append((p3,p4,p5,p6,p7))
        return results

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

    results = []
    for i in range(steps):
        angle = i * stepsize
        results.append(r6sub(angle))
    results.append(results[0])

    d46ref = dismat[i4, i6]
    d46mat = [[getd46rela(ps[1], ps[3], d46ref) for ps in result]
              for result in results]

    results = []
    for i in range(steps):
        for j in range(16):
            if d46mat[i][j] is not None and \
               d46mat[i+1][j] is not None and \
               d46mat[i][j] * d46mat[i+1][j] <= 0:
                angle = rtbis(d46_Resolver(r6sub, j, d46ref),
                              i * stepsize,
                              (i+1) * stepsize,
                              0.1)
                result = r6sub(angle)[j]
                yield {i3: result[0],
                       i4: result[1],
                       i5: result[2],
                       i6: result[3],
                       i7: result[4]}

def getd46rela(p4, p6, d46ref):
    if p4 is None or p6 is None:
        return None
    return (p4 - p6).length() - d46ref

class d46_Resolver:
    def __init__(self, r6sub, mode, d46ref):
        self.r6sub = r6sub
        self.d46ref = d46ref
        self.mode = mode
    def __call__(self, angle):
        result = self.r6sub(angle)[self.mode]
        return (result[1] - result[3]).length() - self.d46ref


def R6(coords, atmidx, dismat, shakedata):
    '''Wrapped R6 algorithm, include R6 and shakeH'''
    shakes = [shakedata[idx] for idx in atmidx[1:-1]]
    for baseresult in R6a(coords, atmidx, dismat):
        newcoords = coords[:]
        for idx, newcoord in baseresult.items():
            newcoords[idx] = newcoord
        for refidxs, sidechain_ in shakes:
            baseresult.update(sidechain.movesidechain(coords, newcoords, refidxs, sidechain_))
        yield baseresult
