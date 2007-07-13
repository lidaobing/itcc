# $Id$

__all__ = ["loopdetect", 'NOLOOP',
           'SIMPLELOOPS', 'COMPLEXLOOPS']
__revision__ = '$Rev$'

# loop types
NOLOOP = 0
SIMPLELOOPS = 1
COMPLEXLOOPS = 2

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
                j = mat[i].tolist().index(1)

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
        return (NOLOOP, [])
    elif deg_max == 2:
        return (SIMPLELOOPS, _countloop2(mat))

    tasks = set()
    ends = set()
    for i in range(len(mat)):
        if trunk_deg[i] > 2:
            ends.add(i)
            for j,v in enumerate(mat[i]):
                if v: tasks.add((i,j))

    res = []
    while tasks:
        i,j = tasks.pop()
        res.append(_countloop3(mat, i, j, ends))
        tasks.remove(tuple(res[-1][:-3:-1]))
    return (COMPLEXLOOPS, res)

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

def _countloop3(mat, beg, next, ends):
    last = beg
    res = [beg, next]
    while next not in ends:
        last, next = next, [i for i in range(len(mat)) if mat[i][next] and i != last][0]
        res.append(next)
    return res

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
    return (looptype, loops)
    """
    connmat = _connectmatrix(mol)
    _delleaf(connmat)
    return _countloop(connmat)

def std_simple_loop(loop):
    if len(loop) < 2: return loop[:]
    idx = loop.index(min(loop))
    res = loop[idx:] + loop[:idx]
    if res[1] > res[-1]:
        res = res[:1] + reversed(res[1:])
    return res

def std_complex_loop(loop):
    if loop[0] < loop[-1]: return loop[:]
    return reversed(loop)

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s xyzfname\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    from itcc.molecule import read
    res = loopdetect(read.readxyz(file(sys.argv[1])))
    if res[0] == NOLOOP:
        print 'NOLOOP'
    elif res[0] == SIMPLELOOPS:
        print 'SIMPLELOOPS'
        for loop in res[1]:
            print ' '.join([str(x+1) for x in std_simple_loop(loop)])
    else:
        print 'COMPLEXLOOPS'
        for loop in res[1]:
            print ' '.join([str(x+1) for x in std_complex_loop(loop)])

if __name__ == '__main__':
    main()
