# $Id$
from itertools import chain

__all__ = ['R6']
__revision__ = '$Rev$'

class R6:
    def __init__(self, data):
        assert len(data) == 7
        self.data = tuple(data)

    def kind(self):
        return tuple([len(node) for node in self.data])

    def needshakenodes(self):
        return tuple(chain(*self.data[1:-1]))
