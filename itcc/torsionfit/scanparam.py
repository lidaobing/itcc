# $Id$
from itcc.torsionfit import ga

__revision__ = '$Rev$'


def foo(list):
    result = 0.0
    for x in list:
        result += x * x
    return result

def scanparam2(list, pos, stepsize, fmark, mark):

    list[pos] += stepsize
    nmark = fmark(list)
    if nmark < mark:
        while nmark < mark:
            mark = nmark
            list[pos] += stepsize
            nmark = fmark(list)
        list[pos] -= stepsize
        return mark

    list[pos] -= 2 * stepsize
    nmark = fmark(list)
    if nmark < mark:
        while nmark < mark:
            mark = nmark
            list[pos] -= stepsize
            nmark = fmark(list)
        list[pos] += stepsize
        return mark

    list[pos] += stepsize
    return None


def scanparam(list, stepsize, fmark):
    n = len(list)
    goodcycle = 0
    pos = 0

    log = file('log', 'a+')

    mark = fmark(list)
    tmpstr = '[' + ', '.join(['%.3f' % x for x in list]) + ']'
    log.write(' %s %.3f\n' % (tmpstr, mark))
    log.flush()

    
    while goodcycle < n:
        nmark = scanparam2(list, pos, stepsize, fmark, mark)
        if nmark is None:
            goodcycle += 1
        else:
            mark = nmark
            goodcycle = 0
            tmpstr = '[' + ', '.join(['%.3f' % x for x in list]) + ']'
            log.write(' %s %.3f\n' % (tmpstr, mark))
            log.flush()
        pos = (pos + 1) % n            
        

if __name__ == '__main__':
    scanparam([0.064, -2.764, 2.672, 1.308, -4.157, -0.089, -1.803, -1.586], 0.001, ga.GA.eval)
    

