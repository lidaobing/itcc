# $Id$

__revision__ = '$Rev$'

class Base:
    def __init__(self, _):
        pass
    
    def getr6s(self, loopatoms):
        doubleloop = loopatoms * 2
        return [tuple([(x,) for x in doubleloop[i:i+7]]) \
                for i in range(len(loopatoms))]
    
    def getcombinations(self, r6s):
        return tuple([(r6,) for r6 in r6s])

