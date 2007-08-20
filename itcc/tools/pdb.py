# $Id$

import numpy

class Pdb(object):
    def __init__(self, ifile):
        self.idxs = []
        self.atoms = []
        self.symbols = []
        self.coords = []
        for line in ifile:
            words = line.split()
            if words[:1] == ['ATOM']:
                self.idxs.append(int(line[7:11]))
                self.symbols.append(line[12:16].strip())
                atom = self.symbols[-1]
                while '0' <= atom[0] <= '9':
                    atom = atom[1:]
                self.atoms.append(atom)
                self.coords.append([float(line[x:x+8]) for x in range(30,54,8)])
        self.idxs = numpy.array(self.idxs)
        self.coords = numpy.array(self.coords)
        
    def connect(self):
        if self.hasattr('connect_data'):
            return self.connect_data
        self.connect_data = [[] for i in range(len(self.atoms))]
        
        
        




            