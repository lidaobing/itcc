# $Id$
"""Crown ether"""

from itcc.CCS2.tors import TorsSet

__revision__ = '$Rev$'

class TSCrown(TorsSet):
    def vary(item):
        doubledata = item * 2
        minusdoubledata = tuple([-x for x in doubledata])
        size = len(item)
        for i in range(0, size, 3):
            yield doubledata[i:i+size]
            yield doubledata[i+size:i:-1]
            yield minusdoubledata[i:i+size]
            yield minusdoubledata[i+size:i:-1]
    vary = staticmethod(vary)

