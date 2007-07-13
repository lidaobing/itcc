# $Id$

__revision__ = '$Rev$'

class Base:
    def __init__(self, _ = None):
        pass
    
    def getr6s(self, loopatoms, is_chain = False):
        if is_chain:
            doubleloop = tuple(loopatoms)
            count = len(doubleloop) - 6
        else:
            doubleloop = tuple(loopatoms) * 2
            count = len(doubleloop) / 2
        for i in range(count):
            yield tuple([(x,) for x in doubleloop[i:i+7]])
    
def _test():
    base = Base()
    print tuple(base.getr6s(range(10)))

if __name__ == '__main__':
    _test()
