# $Id$

try:
    set
except:
    from sets import Set as set

__all__ = ["loopdetect", 'NOLOOP',
           'SIMPLELOOPS', 'COMPLEXLOOPS']
__revision__ = '$Rev$'

# loop types
NOLOOP = 0
SIMPLELOOPS = 1
COMPLEXLOOPS = 2

def is_simpleloop(loop):
    return isinstance(loop[0], int)

def part_loop(loop):
    res = []
    cache = set()
    while len(cache) < len(loop):
        k = (set(loop.keys()) - cache).pop()
        res.append(set([k]))
        c2 = res[-1]
        task = [k]
        
        while task:
            k = task.pop()
            for x in loop[k]:
                if x in c2:
                    continue
                c2.add(x)
                task.append(x)
        cache |= c2
    return res

def delleaf(loop):
    while 1:
        ready = True
        for k, v in loop.items():
            if len(v) == 1:
                loop[v.pop()].remove(k)
                del loop[k]
                ready = False
                break
        if ready:
            break

def split_loop(loop):
    delleaf(loop)
    
    for i1, i2s in loop.items():
        for i2 in i2s:
            if i1 >= i2:
                continue
            if len(i2s) == 2 and len(loop[i2]) == 2:
                continue
            loop2 = loop.copy()
            loop2[i1] = set(loop[i1])
            loop2[i2] = set(loop[i2])
            loop2[i1].remove(i2)
            loop2[i2].remove(i1)
            parts = part_loop(loop2)
            if len(parts) > 1:
                res = []
                for part in parts:
                    partloop = {}
                    for x in part:
                        partloop[x] = loop2[x]
                    res.extend(split_loop(partloop))
                return res
            
    if not loop:
        return []
    
    max_deg = max([len(v) for v in loop.values()])
    if max_deg == 2:
        res = []
        res.append(min(loop.keys()))
        res.append(min(loop[res[0]]))
        while len(res) < len(loop):
            res.append([x for x in loop[res[-1]] if x != res[-2]][0])
        return [res]
    
    tasks = set()
    for k, v in loop.items():
        if len(v) > 2:
            for x in v:
                tasks.add((k, x))
    
    res = []
    while tasks:
        task = tasks.pop()
        res.append(list(task))
        while len(loop(task[-1])) == 2:
            res.append([x for x in loop[task[-1]] if x != task[-2]][0])
        tasks.remove(tuple(res[-1:-3:-1]))
        res[-1] = min(res[-1], res[-1][::-1])
    return [res]

def loopdetect2(mol):
    loop = {}
    for i in range(len(mol)):
        loop[i] = set()
    
    for i in range(len(mol)):
        for j in range(i):
            if mol.is_connect(i, j):
                loop[i].add(j)
                loop[j].add(i)
    
    return split_loop(loop)

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
    res = loopdetect2(read.readxyz(file(sys.argv[1])))
    if not res:
        print 'NOLOOP'
    for x in res:
        try:
            if isinstance(x[0], int):
                print 'SIMPLELOOPS'
                print ' ' + ' '.join([str(y+1) for y in x])
            else:
                print 'COMPLEXLOOPS'
                for x2 in x:
                    print ' ' + ' '.join([str(y+1) for y in x2])
        except:
            print `x`
            raise

if __name__ == '__main__':
    main()
