# $Id$

__revision__ = '$Rev$'

class Base:
    def __init__(self, _ = None):
        pass
    
    def getr6s(self, loopatoms):
        doubleloop = loopatoms * 2
        for i in range(len(loopatoms)):
            yield tuple([(x,) for x in doubleloop[i:i+7]])
    
    def getcombinations(self, r6s):
        for r6 in r6s:
            yield (r6,)

def _test():
    base = Base()
    print tuple(base.getr6s(range(10)))

if __name__ == '__main__':
    _test()
