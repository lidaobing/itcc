# $Id$

from Scientific.Geometry import Vector
from itcc.Tools import cpptools

__revision__ = '$Rev$'

class Shake:
    def __init__(self, func, idxs):
        self.func = func
        self.idxs = idxs
    def __call__(self, coords, distmat):
        return self.func(coords, distmat, self.idxs)

def shakedata(mol, loopatoms):
    neighborlist = mol.neighborlist()
    results = {}

    for atmidx in loopatoms:
        neighbors = neighborlist[atmidx]
        end = [neiidx for neiidx in neighbors if len(neighborlist[neiidx]) == 1]
        nonend = [neiidx for neiidx in neighbors if neiidx not in end]
        type_ = (len(nonend), len(end))
        func = funcidx[type_]
        idxs = [atmidx] + nonend + end
        results[atmidx] = Shake(func, idxs)
    return results

def shake22(coords, distmat, atmidxs):
    assert len(atmidxs) == 5
    p0 = coords[atmidxs[0]]
    p1 = coords[atmidxs[1]]
    p2 = coords[atmidxs[2]]
    r03 = distmat[atmidxs[0], atmidxs[3]]
    r04 = distmat[atmidxs[0], atmidxs[4]]
    p3, p4 = cpptools.shakeH2(tuple(p0.array), tuple(p1.array),
                              tuple(p2.array), r03, r04)
    return {atmidxs[3]: Vector(p3),
            atmidxs[4]: Vector(p4)}

funcidx = {(2, 2): shake22}
