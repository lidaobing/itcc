# $Id$

from itcc.Molecule import tools

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
            assert atomidx not in loop
            if atomidx not in results:
                results.append(atomidx)
                searchs.append(atomidx)
    return results
