# $Id$
from itcc.CCS2.Mezei import R6
from itcc.Tools.tools import length
from itertools import chain


__all__ = ['R6', 'R6_in_vivo']
__revision__ = '$Rev$'

def R6_in_vivo(points):
    assert len(points) == 7
    len1 = [length(points[i], points[i+1])
            for i in range(1,5)]
    len2 = [length(points[i], points[i+2])
            for i in range(0,5)]
    return R6(points[:2] + points[-2:],
              len1, len2)

class R6_:
    def __init__(self, data):
        assert len(data) == 7
        self.data = tuple(data)
        
    def kind(self):
        return tuple([len(node) for node in self.data])

    def needshakenodes(self):
        return tuple(chain(*self.data[1:-1]))
