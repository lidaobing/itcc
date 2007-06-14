# $Id$
from itcc.torsionfit import ga

__revision__ = '$Rev$'


def foo(l):
    result = 0.0
    for x in l:
        result += x * x
    return result

def scanparam2(l, pos, stepsize, fmark, mark):

    l[pos] += stepsize
    nmark = fmark(l)
    if nmark < mark:
        while nmark < mark:
            mark = nmark
            l[pos] += stepsize
            nmark = fmark(l)
        l[pos] -= stepsize
        return mark

    l[pos] -= 2 * stepsize
    nmark = fmark(l)
    if nmark < mark:
        while nmark < mark:
            mark = nmark
            l[pos] -= stepsize
            nmark = fmark(l)
        l[pos] += stepsize
        return mark

    l[pos] += stepsize
    return None


def scanparam(l, stepsize, fmark):
    n = len(l)
    goodcycle = 0
    pos = 0

    log = file('log', 'a+')

    mark = fmark(l)
    tmpstr = '[' + ', '.join(['%.3f' % x for x in l]) + ']'
    log.write(' %s %.3f\n' % (tmpstr, mark))
    log.flush()

    
    while goodcycle < n:
        nmark = scanparam2(l, pos, stepsize, fmark, mark)
        if nmark is None:
            goodcycle += 1
        else:
            mark = nmark
            goodcycle = 0
            tmpstr = '[' + ', '.join(['%.3f' % x for x in l]) + ']'
            log.write(' %s %.3f\n' % (tmpstr, mark))
            log.flush()
        pos = (pos + 1) % n            
        

if __name__ == '__main__':
    scanparam([0.064, -2.764, 2.672, 1.308, -4.157, -0.089, -1.803, -1.586], 0.001, ga.GA.eval)
    

