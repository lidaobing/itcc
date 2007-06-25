# $Id$

import itcc.bodr

__all__ = ["Atom", 'atomsymbol', 'atommass', 'atomchr', 'atomord']
__revision__ = '$Rev$'


_knownAtoms = {}

class Atom(object):
    __slots__ = ['_no', '_type', '_symbol']

    def __new__(cls, no, type_ = 0, symbol = None):
        if isinstance(no, int):
            if symbol is None:
                symbol = atomchr(no)
        elif isinstance(no, str):
            if symbol is None:
                symbol = no
            no = atomord(no)
        else:
            raise ValueError

        key = (no, type_, symbol)
        if key in _knownAtoms:
            return _knownAtoms[key]

        self = object.__new__(cls)
        self._no = no
        self._type = type_
        self._symbol = symbol
        _knownAtoms[key] = self

        return self

    def __getstate__(self):
        return [self._no, self._type, self._symbol]

    def __setstate__(self, state):
        self._no = state[0]
        self._type = state[1]
        self._symbol = state[2]

    def __copy__(self):
        return self
    __deepcopy__ = __copy__

    def __str__(self):
        return self._symbol

    def __repr__(self):
        return "Atom(%i, %i, %s)" % (self._no, self._type, `self._symbol`)

    def getmass(self):
        return atommass[self._no]

    mass = property(getmass)

    def getno(self):
        return self._no
    no = property(getno)

    def gettype(self):
        return self._type
    type = property(gettype)

    def getsymbol(self):
        return self._symbol
    symbol = property(getsymbol)

    def atomchr(self):
        return atomsymbol[self._no]

atomsymbol = ['',
              'H',  'He', 'Li', 'Be', 'B',    # 1- 5
              'C',  'N',  'O',  'F',  'Ne',   # 6-10
              'Na', 'Mg', 'Al', 'Si', 'P',    #11-15
              'S',  'Cl', 'Ar', 'K',  'Ca',   #16-20
              'Sc', 'Ti', 'V',  'Cr', 'Mn',   #21-25
              'Fe', 'Co', 'Ni', 'Cu', 'Zn',   #26-30
              'Ga', 'Ge', 'As', 'Se', 'Br',   #31-35
              'Kr', 'Rb', 'Sr', 'Y',  'Zr',   #36-40
              'Nb', 'Mo', 'Tc', 'Ru', 'Rh',   #41-45
              'Pd', 'Ag', 'Cd', 'In', 'Sn',   #46-50
              'Sb', 'Te', 'I',  'Xe', 'Cs',   #51-55
              'Ba', 'La', 'Ce', 'Pr', 'Nd',   #56-60
              'Pm', 'Sm', 'Eu', 'Gd', 'Tb',   #61-65
              'Dy', 'Ho', 'Er', 'Tm', 'Yb',   #66-70
              'Lu', 'Hf', 'Ta', 'W',  'Re',   #71-75
              'Os', 'Ir', 'Pt', 'Au', 'Hg',   #76-80
              'Tl', 'Pb', 'Bi', 'Po', 'At',   #81-85
              'Rn', 'Fr', 'Ra', 'Ac', 'Th',   #86-90
              'Pa', 'U' , 'Np', 'Pu', 'Am',   #91-95
              'Cm', 'Bk', 'Cf', 'Es', 'Fm',   #96-100
              'Md', 'No', 'Lr', 'Unq','Unp',  #101-105
              'Unh','Uns','Uno','Une']        #106-109

atommass = itcc.bodr.mass

def atomchr(i):
    if 0 < i < len(atomsymbol):
        return atomsymbol[i]
    raise ValueError("atomchr: only support atom index from 1 to 109, inclusive")

def atomord(chr_):
    if len(chr_) == 0:
        raise ValueError
    if len(chr_) == 1:
        key = chr_
    elif chr_[1].islower():
        key = chr_[:2]
    else:
        key = chr_[0]

    try:
        return atomsymbol.index(key)
    except ValueError:
        return 0

if __name__ == '__main__':
    a = Atom(1)
    print a
    print `a`
    import pickle
    ap = pickle.dumps(a)
    print `ap`
    b = pickle.loads(ap)
    print `b`



