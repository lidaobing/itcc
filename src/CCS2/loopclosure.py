# $Id$
import pprint
import bisect
import os.path
import sets
import itertools
from copy import copy
from itcc.Tinker import tinker
from itcc.CCS2 import loopdetect, base, peptide, R6
from itcc.Molecule import read, write
from itcc.Tools import tools

__all__ = ['LoopClosure']
__revision__ = '$Rev$'

class LoopClosure(object):
    def __init__(self, forcefield, keeprange, searchrange):
        self.forcefield = forcefield
        self.keeprange = keeprange
        self.keepbound = None
        self.searchrange = searchrange
        self.searchbound = None
        self.maxsteps = 0
        self.eneerror = 0.0003
        self.moltypekey = None
        
    def __call__(self, molfname):
        self.printparams()
        mol = read.readxyz(file(molfname))
        self.molnametmp = os.path.splitext(molfname)[0] + '.%03i'
        
        moltype = getmoltype(self.moltypekey)(mol)
        self.loopatoms = self.getloopatoms(mol)
        self.r6s = moltype.getr6s(self.loopatoms)
        printr6s(self.r6s)
        self.combinations = moltype.getcombinations(self.r6s)
        self.r6s = tuple(sets.Set(itertools.chain(*self.combinations)))
        printcombinations(self.combinations)
        
        mol, ene = tinker.optimizemol(mol, self.forcefield)
        print '    Potential Surface Map       Minimum ' \
              '%6i %21.4f' % (1, ene)
        print
        self.writemol(1, mol)
        
        self._run(mol, ene)

    def _run(self, mol, ene):
        self.tasks = [(mol, ene)]
        self.enes = [ene]
        self.lowestene = ene
        self.updatebound()
        taskidx = 0

        while taskidx < len(self.tasks):
            initmol, ene = self.tasks[taskidx]
            if self.searchbound is not None and \
                   ene > self.searchbound:
                taskidx += 1
                continue
            
            print
            print ' CCS2 Local Search              Minimum %6i %21.4f' \
                  % (taskidx + 1, ene)
            print
            
            idx = 1
            for mol, ene in self.findneighbor(initmol):
                print '    Search Direction %3i %43.4f' % (idx, ene)
                idx += 1
                if self.keepbound is not None:
                    if ene > self.searchbound:
                        continue
                if self.isnewene(ene):
                    self.tasks.append((mol, ene))
                    self.writemol(len(self.tasks), mol)
                    bisect.insort(self.enes, ene)
                    print
                    print '    Potential Surface Map       Minimum ' \
                          '%6i %21.4f' % (len(self.tasks), ene)
                    print
                    if ene < self.lowestene:
                        self.lowestene = ene
                        self.updatebound()
            taskidx += 1
            print

    def getloopatoms(self, mol):
        loops = loopdetect(mol)
        assert len(loops) == 1
        return loops[0]

    def printparams(self):
        print 'Forcefield: %s' % self.forcefield
        print 'KeepRange: %s' % self.keeprange
        print 'SearchRange: %s' % self.searchrange
        print

    def writemol(self, idx, mol):
        ofname = self.molnametmp % idx
        ofile = file(ofname, 'w+')
        write.writexyz(mol, ofile)
        ofile.close()

    def updatebound(self):
        if self.searchrange is not None:
            self.searchbound = self.lowestene + self.searchrange
        if self.keeprange is not None:
            self.keepbound = self.lowestene + self.keeprange

    def isnewene(self, ene):
        idx = bisect.bisect(self.enes, ene)
        if idx - 1 >= 0 and \
               abs(self.enes[idx-1] - ene) < self.eneerror:
            return False
        if idx < len(self.enes) and \
               abs(self.enes[idx] - ene) < self.eneerror:
            return False
        return True

    def findneighbor(self, mol):
        mol.builddistancematrix()
        coords = mol.coords
        dismat = mol.distancematrix
        r6results = {}
        for r6 in self.r6s:
            r6results[r6] = getr6result(coords, r6, dismat)
        for combine in self.combinations:
            r6s = [r6results[r6] for r6 in combine]
            result = list(tools.combinecombine(r6s))
            for molresult in result:
                newmol = copy(mol)
                for r6result in molresult:
                    for idx, coord in r6result.items():
                        newmol.coords[idx] = coord
                yield tinker.minimizemol(newmol, self.forcefield)

def getr6result(coords, r6, dismat):
    if r6type(r6) == (1,1,1,1,1,1,1):
        idxs = tuple(itertools.chain(*r6))
        return R6.R6(coords, idxs, dismat)
    assert False, r6type(r6)

def r6type(r6):
    return tuple([len(x) for x in r6])

moltypedict = {'peptide': peptide.Peptide}
def getmoltype(key):
    return moltypedict.get(key, base.Base)
    
def printr6s(r6s):
    print "This loop has %i R6 blocks:" % len(r6s)
    pprint.pprint(r6s)
    print
    
def printcombinations(combinations):
    print "These R6 blocks have %i kinds of combination:" % len(combinations)
    for i, combination in enumerate(combinations):
        print "Combination-%i: %s" % (i, combination)
    print
            
            
            
            
