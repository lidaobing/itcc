from itcc.CCS2.Mezei import R6
from itcc.Tools.tools import length


__all__ = ['R6', 'R6_in_vivo']

def R6_in_vivo(points):
    assert len(points) == 7
    len1 = [length(points[i], points[i+1])
            for i in range(1,5)]
    len2 = [length(points[i], points[i+2])
            for i in range(0,5)]
    return R6(points[:2] + points[-2:],
              len1, len2)
    
        

