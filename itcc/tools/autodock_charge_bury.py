# $Id$

import sys
import math
from cStringIO import StringIO

from itcc.tools import dlg, pdbq_large_charge
from itcc.tools.pdb import Pdb
from itcc.tools import c60

def disq(coord1, coord2):
    return sum((coord1-coord2)**2)

def expose_area(protein, ligand, atoms):
    r1 = 4.0
    r2 = 3.3
    r2o = 2.6
    r2h = 1.8
    
    r2q = r2 * r2
    r2oq = r2o * r2o
    r2hq = r2h * r2h
    
    pro_coords_o = protein.coords.take([i for i in range(len(protein.atoms)) if protein.atoms[i][0] in 'Oo' ],
                                      axis=0)
    pro_coords_h = protein.coords.take([i for i in range(len(protein.atoms)) if protein.atoms[i][0] == 'H' ],
                                      axis=0)
    pro_coords_other = protein.coords.take([i for i in range(len(protein.atoms)) if protein.atoms[i][0] not in 'HOo' ],
                                      axis=0)
    
    
    ress = []
    for atom in atoms:
        coord = ligand.coords[atom.idx]
        coords = [x for x in (c60.c60()* r1 + coord)]
        for i in range(len(ligand.atoms)):
            if i == atom.idx:
                continue
            for idx in range(len(coords))[::-1]:
                coord = coords[idx]
                try:
                    if (ligand.atoms[i] == 'H' and disq(coord, ligand.coords[i]) <= r2hq) \
                        or (ligand.atoms[i] != 'H' and disq(coord, ligand.coords[i]) <= r2q):
                        del coords[idx]
                except:
                    print i
                    raise
        
        res = 0
        
        for coord in coords:
            ok = True
            for pro_coords, rq in ((pro_coords_o, r2oq), (pro_coords_other, r2q), (pro_coords_h, r2hq)):
                if min(((pro_coords - coord) ** 2).sum(axis=1)) < rq:
                    ok = False
                    break
            if ok:
                res += 1
        ress.append(res)
        print atom.idx+1, ligand.atoms[atom.idx], res
    return ress
#                
#        for i in range(len(protein.atoms)):
#            for idx in range(len(coords))[::-1]:
#                coord = coords[idx]
#                if (protein.atoms[i] == 'H' and disq(coord, protein.coords[i]) <= r2hq) \
#                    or (protein.atoms[i] != 'H' and disq(coord, protein.coords[i]) <= r2q):
#                    del coords[idx]
        

def main():
    if len(sys.argv) != 3:
        import os.path
        sys.stderr.write('Usage: %s foo.pdbqs foo.dlg\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    ifile1 = sys.stdin
    if sys.argv[1] != '-':
        ifile1 = file(sys.argv[1])
        
    ifile2 = sys.stdin
    if sys.argv[2] != '-':
        ifile2 = file(sys.argv[2])
    
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
        res = expose_area(pdb, x2, charges)
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
