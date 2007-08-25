# $Id$

import sys
import math
import random
from cStringIO import StringIO

import numpy

from itcc.tools import dlg, pdbq_large_charge
from itcc.tools.pdb import Pdb
from itcc.tools import ball_200, ball_60



class Param(object):
    def __init__(self, r1l=3.0, r1h = 3.5, step=0.2, r2=3.0, r2o=2.5, r2h=1.8):
        self.step = step
        self.stepcount = int(round((r1h-r1l)/step)+1)
        self.r1l = r1l
        self.r1h = r1h
        self.r2 = r2
        self.r2o = r2o
        self.r2h = r2h
        self.r2q = r2 * r2
        self.r2oq = r2o * r2o
        self.r2hq = r2h * r2h
        
params = {'H': Param(r1l=1.7, r1h = 2.3),
          'O': Param(r1l=2.8, r1h = 3.3),
          'o': Param(),
          }

def disq(coord1, coord2):
    return sum((coord1-coord2)**2)

def is_solvent(pro_coords_o, pro_coords_h, pro_coords_other, ligand, coord_water):
    r = 2.8
    min_count = 3
    coords = [x for x in (ball_60.data* r + coord_water)]
    param = params['O']
    for i in range(len(ligand.atoms)):
        for idx in range(len(coords))[::-1]:
            coord = coords[idx]
            if (ligand.atoms[i][0] == 'H' and disq(coord, ligand.coords[i]) <= param.r2hq) \
                or (ligand.atoms[i][0] in 'OoN' and disq(coord, ligand.coords[i]) <= param.r2oq) \
                or (ligand.atoms[i][0] not in 'HOoN' and disq(coord, ligand.coords[i]) <= param.r2q):
                del coords[idx]

    res = []
    for coord in coords:
        ok = True
        for pro_coords, rq in ((pro_coords_o, param.r2oq), (pro_coords_other, param.r2q), (pro_coords_h, param.r2hq)):
            if min(((pro_coords - coord) ** 2).sum(axis=1)) < rq:
                ok = False
                break
        if ok:
	    res.append(coord)
	    if len(res) >= min_count:
	        return True
    return False

def find_water(pro_coords_o, pro_coords_h, pro_coords_other, ligand, idx):
    param = params[ligand.atoms[idx][0]]
    coords = []
    for i in range(param.stepcount):
        r = param.r1l + i * param.step
        coords.extend([x for x in (ball_200.data* r + ligand.coords[idx])])

    for i in range(len(ligand.atoms)):
        for idx in range(len(coords))[::-1]:
            coord = coords[idx]
            if (ligand.atoms[i][0] == 'H' and disq(coord, ligand.coords[i]) <= param.r2hq) \
                or (ligand.atoms[i][0] in 'OoN' and disq(coord, ligand.coords[i]) <= param.r2oq) \
                or (ligand.atoms[i][0] not in 'HOoN' and disq(coord, ligand.coords[i]) <= param.r2q):
                del coords[idx]

    res = []
    for coord in coords:
        ok = True
        for pro_coords, rq in ((pro_coords_o, param.r2oq), (pro_coords_other, param.r2q), (pro_coords_h, param.r2hq)):
            if min(((pro_coords - coord) ** 2).sum(axis=1)) < rq:
                ok = False
                break
        if ok:
            res.append(coord)
            
    return res

def merge_water(waters):
    min_dis = 1.4
    min_dis_sq = min_dis * min_dis
    res = []
    for coord1 in waters:
        is_new = True
        for i, x in enumerate(res):
            coord2, c = x
            if disq(coord1, coord2) <= min_dis_sq:
                coord2 = (coord2 * c + coord1) / (c+1)
                res[i] = (coord2, c+1)
                is_new = False
                break
        if is_new:
            res.append((coord1, 1))
    return [x[0] for x in res]

def merge_water_2(waters):
    while 1:
        len1 = len(waters)
        waters = merge_water(waters)
        if len1 == len(waters):
            return waters

def expose_area(protein, ligand, atoms, verbose=0):
    pro_coords_o = protein.coords.take([i for i in range(len(protein.atoms)) if protein.atoms[i][0] in 'OoN' ],
                                      axis=0)
    pro_coords_h = protein.coords.take([i for i in range(len(protein.atoms)) if protein.atoms[i][0] == 'H' ],
                                      axis=0)
    pro_coords_other = protein.coords.take([i for i in range(len(protein.atoms)) if protein.atoms[i][0] not in 'HOoN' ],
                                      axis=0)
    
    
    resss = []
    for atom in atoms:
        res = False
        for active in atom.actives:
            waters = find_water(pro_coords_o, pro_coords_h, pro_coords_other, ligand, active)
            waters = merge_water_2(waters)
            for water in waters:
                if is_solvent(pro_coords_o, pro_coords_h, pro_coords_other, ligand, water):
                    res = True
                    break
            if res:
                break
        resss.append(res)
        print atom.idx+1, ligand.atoms[atom.idx], int(res)
    return resss
    
#                    
#            typ = ligand.atoms[active][0]
#            param = params[typ]
#            coord = ligand.coords[active]
#    #        coords = [x for x in (c60.c60()* (param.r1l + param.r1h) / 2.0 + coord)]
#            coords = []
#            while len(coords) < count:
#                t1 = numpy.array([random.uniform(-param.r1h, param.r1h) for i in range(3)])
#                lensq = sum(t1 * t1)
#                if param.r1l * param.r1l <= lensq <= param.r1h * param.r1h:
#                    coords.append(coord + t1)
#                
#            for i in range(len(ligand.atoms)):
#                if i == active:
#                    continue
#                for idx in range(len(coords))[::-1]:
#                    coord = coords[idx]
#                    try:
#                        if (ligand.atoms[i][0] == 'H' and disq(coord, ligand.coords[i]) <= param.r2hq) \
#                            or (ligand.atoms[i][0] in 'OoN' and disq(coord, ligand.coords[i]) <= param.r2oq) \
#                            or (ligand.atoms[i][0] not in 'HOoN' and disq(coord, ligand.coords[i]) <= param.r2q):
#                            del coords[idx]
#                    except:
#                        print i
#                        raise
#            
#            res = 0
#            
#            for coord in coords:
#                ok = True
#                for pro_coords, rq in ((pro_coords_o, param.r2oq), (pro_coords_other, param.r2q), (pro_coords_h, param.r2hq)):
#                    if min(((pro_coords - coord) ** 2).sum(axis=1)) < rq:
#                        ok = False
#                        break
#                if ok:
#                    res += 1
#                    if verbose >= 1:
#                        print 'HETATM   %2i  O   HOH    %2i    %8.3f%8.3f%8.3f  1.00  0.0.0' % (res, res, coord[0], coord[1], coord[2])
#            ress.append(res)
#            print active+1, ligand.atoms[active], res
#        resss.append(sum(ress)/len(ress))
#        print atom.idx+1, ligand.atoms[atom.idx], resss[-1]
#        print
#    return resss
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
            if not y:
                dE += 2.0 * abs(charges[i].charge)
        print '%s\t%s\t%s\t%s' % (x.rank, x.ene, dE, x.ene+dE)
	break

if __name__ == '__main__':
    main()
