# $Id$

import exceptions

class Error(exceptions.Exception):
    pass

def rtbis(func, x1, x2, xacc):
    "Reference: Numerical Recipes in C, Chapter 9.1, Page 354"
    f = func(x1)
    fmid = func(x2)
    if not isinstance(f, float) or not isinstance(fmid, float):
        raise Error()
    if f * fmid >= 0:
        raise Error()

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
        if not isinstance(fmid, float):
            raise Error()
        if fmid <= 0.0:
            rtb = xmid
        if abs(dx) < xacc or fmid == 0.0:
            return rtb
    raise Error() # never get here

