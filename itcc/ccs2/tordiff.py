# $Id$

# TODO: need a testcase for this module

import math
from itcc.tools import periodnumber

def torsdiff(tors1, tors2,
            is_achiral = False,
            head_tail = -1,
            loop_step = 0):
    '''\
torsdiff(tors1, tors2,
            is_achiral = False,
            head_tail = -1,
            loop_step = 0)
            
\param tors1, unit is radian
\param tors2, unit is radian
\param is_achiral if true, tor->[-x for x in tor]
\param head_tail if not -1, tor->(tor[head_tail:] + tor[:head_tail])[::-1]
\param loop_step if not zero, means tor->tor[loop_step:] + tor[:loop_step]
    '''
    tors1 = list(tors1)
    tors2 = list(tors2)
    
    if len(tors1) != len(tors2):
        raise ValueError, "len(tors1) != len(tors2)"
    
    if loop_step < 0:
        raise ValueError, "loop_step < 0"
    
    if loop_step != 0:
        if len(tors1) % loop_step != 0:
            raise ValueError, "len(tors1) % loop_step != 0"
        
    tors2s = [tors2]
    if head_tail != -1:
        tors2s += [(x[head_tail:] + x[:head_tail])[::-1] for x in tors2s]
    if is_achiral:
        tors2s += [[-y for y in x] for x in tors2s]
    if loop_step != 0:
        n = len(tors2s)
        for i in range(len(tors1)/loop_step - 1):
            tors2s += [x[loop_step:] + x[:loop_step] for x in tors2s[-n:]]
            
    return min([tordiff(tors1, x) for x in tors2s])

def tordiff(tors1, tors2):
    Angle = periodnumber.genPNclass(-math.pi, math.pi)
    return max([abs(Angle(x1-x2)) for x1, x2 in zip(tors1, tors2)])
