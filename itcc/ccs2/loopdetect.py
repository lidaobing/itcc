# $Id$

__all__ = ["loopdetect"]
__revision__ = '$Rev$'

def _symmatp(mat):
    """_symmatp(mat) -> Bool
    if mat[i][j] == mat[j][i]:
        return True
    """
    for i in range(len(mat)):
        for j in range(i+1, len(mat)):
            if mat[i][j] != mat[j][i]:
                return False
    return True

def _diagonalzerop(mat):
    for i in range(len(mat)):
        if mat[i][i] != 0:
            return False
    return True

def _delleaf(mat):
    """_delleaf(mat) -> degrees
    del the leaf node, only preserve the cyclic part.
    the mat is modified.
    """
    degrees = sum(mat)
    finished = False
    while not finished:
        finished = True
        for i in range(len(degrees)):
            if degrees[i] == 1:
                finished = False

                j = [k for k in range(len(degrees)) if mat[i][k] == 1]
                assert(len(j) == 1)
                j = j[0]

                mat[i][j] = 0
                mat[j][i] = 0
                degrees[i] = 0
                degrees[j] -= 1
    return degrees

def _countloop(mat):
    trunk_deg = sum(mat)
    deg_max = max(trunk_deg)
    assert(deg_max != 1)
    if deg_max == 0:
        return []
    elif deg_max == 2:
        return _countloop2(mat)
    else:
        raise RuntimeError, "I can't deal with molecule with complex cycle."

def _countloop2(mat):
    trunk_deg = sum(mat).tolist()
    result = []
    while True:
        try:
            i = trunk_deg.index(2)
        except ValueError:
            break
        result.append([i])

        while True:
            j = mat[i].tolist().index(1)

	    # break the connect between i and j
            mat[i][j] = 0
            mat[j][i] = 0
            trunk_deg[i] -= 1
            trunk_deg[j] -= 1

            if j == result[-1][0]:
                break

            result[-1].append(j)
            i = j
    return result

def _connectmatrix(mol):
    """_connectmatrix(mol) -> Matrix
    build the connectmatrix of mol.
    """
    connmat = mol.connect.copy()

    if not (_symmatp(connmat) and _diagonalzerop(connmat)):
        raise RuntimeError

    return connmat


def loopdetect(mol):
    """loopdetect(mol):
    return the loops in mol
    """
    connmat = _connectmatrix(mol)
    _delleaf(connmat)
    return _countloop(connmat)
