# $Id$

__revision__ = '$Rev$'
__all__ = ['genPNclass']

def genPNclass(llimit, ulimit):
    assert llimit < ulimit
    class Periodnumber:
        def __init__(self, data):
            gap = ulimit - llimit
            self.data = (data - llimit) % gap + llimit

        def __float__(self):
            return self.data

        def __str__(self):
            return str(self.data)

        def __repr__(self):
            return '%s(%s)' % (self.__class__.__name__, repr(self.data))

        def __add__(self, other):
            return self.__class__(self.data + float(other))

        def __sub__(self, other):
            return self.__class__(self.data - float(other))

        def __neg__(self):
            return self.__class__(-self.data)

        def __abs__(self):
            return abs(self.data)
    return Periodnumber


