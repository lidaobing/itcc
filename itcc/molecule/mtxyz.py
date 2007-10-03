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

    def read_mol_as_string(self):
        result = ""
        cur = 0
        need = None
        for line in self._ifile:
            if cur == 0:
                need = int(line.split()[0]) + 1
            result += line
            cur += 1
            if cur == need:
                yield result
                result = ""
                cur = 0
                need = None

def read_mtxyz_frame(ifile, frame_idx):
    assert frame_idx >= 0

            

        
