# $Id$
"""extend Mezei's method to protein.
"""
import math
from itcc.CC2 import pyramid
from itcc.CC2 import config

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
    threshold = config.get('Mezei_p24_threshold', -0.01*0.01)
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
            continue
        newcoords = coords[:]
        newcoords[i3] = i3coord
        i2coords = wrappyramid((i2, i1, i3, i4), newcoords, dismat)
        if i2coords[0] is None:
            result.append((None, None))
            continue
        assert (i2coords[0] - i2coords[1]).length() < 0.01
        result.append((i2coords[0], i3coord))
    return result

def R6a(atmidx, coords, dismat):
    '''resolve a fragment of protein:
    N1-C2-C3(=O)-N4-C5-C6(=O)-N7-C8-C9(=O)
   
    known the coords of p1, p2, p8, p9, and all the bond length and
    bond length and bond angles, to calculate the coords from p3 to p7
    '''
    i1, i2, i3, i4, i5, i6, i7, i8, i9 = atmidx
    p5o, p5x, p5y = wrappyramid2((i5, i2, i8), coords, dismat)

    steps = config.config.get('Mezei_R6_steps', 36)
    stepsize = 2 * math.pi / steps

    results = []
    for i in range(steps):
        results.append([])
        angle = i * stepsize
        p5 = p5o + p5x * math.cos(angle) + p5y * math.sin(angle)
        newcoords = coords[:]
        coords[i5] = p5
        for p4, p3 in propyramida((i5, i4, i3, i2, i1), newcoords, dismat):
            if p4 is None:
                results[-1].append((None,)*5)
                results[-1].append((None,)*5)
                continue
            for p6, p7 in propyramida((i5, i6, i7, i8, i9), newcoords, dismat):
                if p6 is None:
                    results[-1].append((None,)*5)
                    continue
            results[-1].append((p3,p4,p5,p6,p7))

    results.append(results[0])
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
