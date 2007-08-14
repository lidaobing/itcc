# $Id$

if not hasattr(__builtins__, 'set'):
    from sets import Set as set

__all__ = ["loopdetect", 'pick_largest_simpleloop']

class Error(Exception):
    pass
    

def is_simpleloop(loop):
    return isinstance(loop[0], int)

def is_allsimpleloop(loops):
    for loop in loops:
        if not is_simpleloop(loop):
            return False
    return True

def pick_largest_simpleloop(loops):
    if not loops:
        raise Error("no loop")
    if not is_allsimpleloop(loops):
        raise Error("some loop is not simple loop")
    lens = [len(x) for x in loops]
    lens.sort()
    if len(lens) >= 2 and lens[-1] == lens[-2]:
        raise Error("there is a tie between laargest simple loop")
    return [x for x in loops if len(x) == lens[-1]][0]

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
        while len(loop[res[-1][-1]]) == 2:
            res[-1].append([x for x in loop[res[-1][-1]] if x != res[-1][-2]][0])
        tasks.remove(tuple(res[-1][-1:-3:-1]))
        res[-1] = min(res[-1], res[-1][::-1])
    return [res]

def loopdetect(mol):
    loop = {}
    for i in range(len(mol)):
        loop[i] = set()
    
    for i in range(len(mol)):
        for j in range(i):
            if mol.is_connect(i, j):
                loop[i].add(j)
                loop[j].add(i)
    
    return split_loop(loop)

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s xyzfname\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    from itcc.molecule import read
    res = loopdetect(read.readxyz(file(sys.argv[1])))
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
