# $Id$

from itcc.molecule import tools
from itcc.ccs2 import pyramid

__revision__ = '$Rev$'

def getsidechain(mol, loop, idx):
    assert idx in loop
    neighborlist = tools.neighborlist(mol)
    searchs = [atomidx for atomidx in neighborlist[idx]
               if atomidx not in loop]
    results = searchs[:]
    while searchs:
        search = searchs.pop()
        for atomidx in neighborlist[search]:
            if atomidx == idx:
                continue
            if atomidx in loop:
                continue
            if atomidx not in results:
                results.append(atomidx)
                searchs.append(atomidx)
    return results

def movesidechain(fromcoords, tocoords, refidxs, sidechain):
    assert len(refidxs) == 3
    reffrom = [fromcoords[idx] for idx in refidxs]
    refto = [tocoords[idx] for idx in refidxs]
    trans1, _ = pyramid.construct_both_transform_matrix(*reffrom)
    _, trans2 = pyramid.construct_both_transform_matrix(*refto)
    totaltrans = trans2 * trans1
    result = {}
    for idx in sidechain:
        result[idx] = totaltrans(fromcoords[idx])
    return result
