# $Id$

import sys
import math
import random
from cStringIO import StringIO

import numpy

from itcc.tools import dlg, pdbq_large_charge
from itcc.tools.pdb import Pdb
from itcc.tools import c60

class Param(object):
    def __init__(self, r1l=3.0, r1h = 3.5, r2=3.0, r2o=2.5, r2h=1.8):
        self.r1l = r1l
        self.r1h = r1h
        self.r2 = r2
        self.r2o = r2o
        self.r2h = r2h
        self.r2q = r2 * r2
        self.r2oq = r2o * r2o
        self.r2hq = r2h * r2h

def disq(coord1, coord2):
    return sum((coord1-coord2)**2)

def max_distance(coords):
    res = 0.0
    for i in range(len(coords)):
        for j in range(i):
            t = coords[i] - coords[j]
            res = max(res, sum(t*t))
    return math.sqrt(res)

def expose_area(protein, ligand, atoms, verbose=0):
    count = 200
    params = {'P': Param(r1l=3.4, r1h = 4.0),
              'S': Param(r1l=3.5, r1h = 4.0),
              'N': Param(r1l=2.6, r1h = 3.2),
              'CO': Param(r1l=3.5, r1h = 4.0),
              'CN': Param(r1l=3.5, r1h = 4.0),
              }
    
    pro_coords_o = protein.coords.take([i for i in range(len(protein.atoms)) if protein.atoms[i][0] in 'OoN' ],
                                      axis=0)
    pro_coords_h = protein.coords.take([i for i in range(len(protein.atoms)) if protein.atoms[i][0] == 'H' ],
                                      axis=0)
    pro_coords_other = protein.coords.take([i for i in range(len(protein.atoms)) if protein.atoms[i][0] not in 'HOoN' ],
                                      axis=0)
    
    
    ress = []
    for atom in atoms:
        try:
            param = params[atom.type]
        except:
            print atom.__dict__
        coord = ligand.coords[atom.idx]
#        coords = [x for x in (c60.c60()* (param.r1l + param.r1h) / 2.0 + coord)]
        coords = []
        while len(coords) < count:
            t1 = numpy.array([random.uniform(-param.r1h, param.r1h) for i in range(3)])
            lensq = sum(t1 * t1)
            if param.r1l * param.r1l <= lensq <= param.r1h * param.r1h:
                coords.append(coord + t1)
            
        for i in range(len(ligand.atoms)):
            if i == atom.idx:
                continue
            for idx in range(len(coords))[::-1]:
                coord = coords[idx]
                try:
                    if (ligand.atoms[i][0] == 'H' and disq(coord, ligand.coords[i]) <= param.r2hq) \
                        or (ligand.atoms[i][0] in 'OoN' and disq(coord, ligand.coords[i]) <= param.r2oq) \
                        or (ligand.atoms[i][0] not in 'HOoN' and disq(coord, ligand.coords[i]) <= param.r2q):
                        del coords[idx]
                except:
                    print i
                    raise
        
        res = 0
        res2 = []
        
        for coord in coords:
            ok = True
            for pro_coords, rq in ((pro_coords_o, param.r2oq), (pro_coords_other, param.r2q), (pro_coords_h, param.r2hq)):
                if min(((pro_coords - coord) ** 2).sum(axis=1)) < rq:
                    ok = False
                    break
            if ok:
                res += 1
                res2.append(coord)
                if verbose >= 1:
                    print 'HETATM   %2i  O   HOH    %2i    %8.3f%8.3f%8.3f  1.00  0.0.0' % (res, res, coord[0], coord[1], coord[2])
        if res and verbose >= 1:
            print 'TER'
        ress.append(res)
        
        max_dis = max_distance(res2)
        print atom.idx+1, ligand.atoms[atom.idx], res, max_dis
    return ress
#                
#        for i in range(len(protein.atoms)):
#            for idx in range(len(coords))[::-1]:
#                coord = coords[idx]
#                if (protein.atoms[i] == 'H' and disq(coord, protein.coords[i]) <= r2hq) \
#                    or (protein.atoms[i] != 'H' and disq(coord, protein.coords[i]) <= r2q):
#                    del coords[idx]
        

def main():
    args = sys.argv[1:]
    
    verbose = 0
    if args and args[0] == '-v':
        verbose = 1
        args = args[1:]
    
    if len(args) != 2:
        import os.path
        sys.stderr.write('Usage: %s [-v] foo.pdbqs foo.dlg\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    ifile1 = sys.stdin
    if args[0] != '-':
        ifile1 = file(args[0])
        
    ifile2 = sys.stdin
    if args[1] != '-':
        ifile2 = file(args[1])
    
    sys.stdout.flush()
    aDlg = dlg.Dlg(ifile2)
    
    charges = None
    
    pdb = Pdb(ifile1)
    proccessed_rank = set()
    print "rank\tE\tdE\tnewE"
    for x in aDlg:
        if x.rank in proccessed_rank:
            continue
	if x.rank != 1:
	    continue
        if charges is None:
            charges = pdbq_large_charge.pdbq_large_charge(StringIO(x.mol))
        x2 = Pdb(StringIO(x.mol))
        res = expose_area(pdb, x2, charges, verbose)
        dE = 0.0
        for i, y in enumerate(res):
            if y == 0:
                dE += 2.0 * abs(charges[i].charge)
            elif 1 <= y <= 2:
                dE += 1.0 * abs(charges[i].charge)
        print '%s\t%s\t%s\t%s' % (x.rank, x.ene, dE, x.ene+dE)
	break

if __name__ == '__main__':
    main()
