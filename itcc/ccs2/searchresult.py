'''store CCS2 search result'''

__revision__ = '0.1'

class SearchResult:
    '''store CCS2 search result, include mol, ene, opttimes'''
    def __init__(self, mol, ene, opttimes):
        self.mol = mol
        self.ene = ene
        self.opttimes = opttimes
    def __cmp__(self, other):
        return cmp(self.ene, other)
