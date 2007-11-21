import sys
import os.path

from itcc.core import tools
from itcc.molecule import read, write, molecule
from itcc.molecule.atom import Atom

class AddMethyl(object):
    methyl_n_type = 86
    methyl_c_type = 90
    methyl_h_type = 6
    
    def add_one_methyl(self, mol, idx):
        h_idx = None
        for i in range(len(mol)):
            if mol.connect[idx, i] and mol.atoms[i].no == 1:
                h_idx = i
                break

        mol.atoms[idx] = Atom(7, self.methyl_n_type)
        if h_idx is None:
            raise RuntimeError("there is no hydrogen near the atom %i"
                               % idx)
        mol.atoms[h_idx] = Atom(6, self.methyl_c_type)
        
        atom_h = Atom(1, self.methyl_h_type)
        connect = mol.connect
        for i in range(3):
            coord = mol.coords[h_idx] + molecule.CoordType(tools.random_vector())
            mol.addatom(atom_h, coord)

        oldlen = len(connect)
        for i in range(oldlen):
            for j in range(i):
                if connect[i,j]:
                    mol.buildconnect(i, j)
        
        for i in range(3):
            mol.buildconnect(len(mol)-1-i, h_idx)

    def __call__(self, ifile, ofile, idxs):
        mol = read.readxyz(ifile)

        ns = []

        for i in range(len(mol)):
            if mol.atoms[i].no == 7:
                ns.append(i)

        for i in idxs:
            assert i < len(ns)
            self.add_one_methyl(mol, ns[i])

        write.writexyz(mol, ofile)

addmethyl = AddMethyl()

def usage(ofile):
    u =     'Usage: %s <FILE> <IDX>...\n' \
            '  <IDX> is 1-based.\n'
         
    ofile.write(u % os.path.basename(sys.argv[0]))

def main():
    if len(sys.argv) < 3:
        usage(sys.stderr)
        sys.exit(1)

    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])

    idxs = [int(x) - 1 for x in sys.argv[2:]]

    addmethyl(ifile, sys.stdout, idxs)

if __name__ == '__main__':
    main()
