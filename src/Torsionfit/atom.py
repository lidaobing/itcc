# $Id$
# $Log: atom.py,v $
# Revision 1.6  2004/08/27 13:19:59  nichloas
# add Atom.__str__ and Atom.__repr__
#
# Revision 1.5  2004/06/03 08:44:09  nichloas
# * atomord函数中的KeyError改为ValueError
#
# Revision 1.4  2004/02/16 11:52:07  nichloas
# fix: Atom.__init__ not set symbol properly
#
# Revision 1.3  2004/02/01 05:01:33  nichloas
# add Atom.copy()
#
# Revision 1.2  2003/11/28 07:00:58  nichloas
# add header
#

import pickle

class Atom(object) :
    def __init__(self, no = 0, type = 0):
        self.no = no
        self.type = type
        self.x = self.y = self.z = 0.0

    def copy(self):
        "return a copy of self"
        return pickle.loads(pickle.dumps(self, pickle.HIGHEST_PROTOCOL))

    def getsymbol(self):
        return self._symbol

    def setsymbol(self, value):
        self._symbol = value
        self._no = atomord(value)

    symbol = property(getsymbol, setsymbol)

    def getno(self):
        return self._no
    def setno(self, value):
        self._no = value
        self._symbol = atomchr(value)

    no = property(getno, setno)

    def getmass(self):
        return atommass[self._no]

    mass = property(getmass)
        
    def getcoords(self):
        return [self.x,self.y,self.z]

    def setcoords(self, value):
        assert(len(value) == 3)
        self.x = float(value[0])
        self.y = float(value[1])
        self.z = float(value[2])

    coords = property(getcoords, setcoords)
    

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else :
            raise IndexError

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else :
            raise IndexError

    def __str__(self):
        return "(%2s%8.3f%8.3f%8.3f)" % (self._symbol, self.x, self.y, self.z)

    __repr__ = __str__

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

atommass = [0,
            1.0079, 4.0026,  6.941,   9.01218,   10.81,  # 1- 5
            12.011, 14.0067, 15.9994, 18.998403, 20.179] # 6-10

def atomchr(i):
    return atomsymbol[i]

def atomord(chr):
    if len(chr) == 0:
        return None
    
    if len(chr) == 1:
        key = chr
    elif chr[1].isupper():
        key = chr[0]
    else:
        key = chr[:2]
    
    try:
        return atomsymbol.index(key)
    except ValueError:
        return None

                
        
