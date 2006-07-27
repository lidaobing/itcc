# $Id$

'''Deal with multi tinker xyz file, such as TINKER .arc file.
'''

__revision__ = '$Rev$'

from itcc.molecule import read

class Mtxyz:
    def __init__(self, ifile):
        self._ifile = ifile

    def __iter__(self):
        return self

    def next(self):
        try:
            return read.readxyz(self._ifile)
        except:
            raise StopIteration
