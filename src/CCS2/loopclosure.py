# $Id$
import os
import os.path
import bisect
import heapq
import sets
import pprint
import itertools
import time
from itcc.Tinker import tinker
from itcc.CCS2 import loopdetect, base, peptide, R6, Mezei, shake
from itcc.Molecule import read, write, tools as moltools
from itcc.Tools import tools

__all__ = ['LoopClosure']
__revision__ = '$Rev$'

class LoopClosure(object):
    def __init__(self, forcefield, keeprange, searchrange):
        self.forcefield = forcefield
        self.keeprange = keeprange
        self.searchrange = searchrange
        self.maxsteps = None
        self.eneerror = 0.0003
        self.moltypekey = None
        self.tasks = []
        self.taskheap = []
        self.enes = []
        self.minconverge = 0.001
        self.molnametmp = None
        self.newmolnametmp = None
        self.lowestene = None
        self.step = 0
        self.shakedata = None

    def getkeepbound(self):
        if self.keeprange is None:
            return None
        return self.lowestene + self.keeprange
    keepbound = property(getkeepbound)

    def getsearchbound(self):
        if self.searchrange is None:
            return None
        return self.lowestene + self.searchrange
    searchbound = property(getsearchbound)

    def __call__(self, molfname):
        self.printparams()
        mol = read.readxyz(file(molfname))
        self.newmolnametmp = os.path.splitext(molfname)[0] + '.%03i'
        self.molnametmp = os.path.splitext(molfname)[0] + '.tmp.%03i'
        typedmol = getmoltype(self.moltypekey)(mol)
        self.loopatoms = self.getloopatoms(mol)
        self.shakedata = shake.shakedata(mol, self.loopatoms)
        self.r6s = typedmol.getr6s(self.loopatoms)
        printr6s(self.r6s)
        self.combinations = typedmol.getcombinations(self.r6s)
        self.r6s = tuple(sets.Set(itertools.chain(*self.combinations)))
        printcombinations(self.combinations)

        mol, ene = tinker.minimizemol(mol, self.forcefield, self.minconverge)
        self.lowestene = ene
        self.addtask(mol, ene)
        for taskidx in self.taskqueue():
            self.runtask(taskidx)
        self.reorganizeresults()

    def runtask(self, taskidx):
        mol, ene = self.tasks[taskidx]
        print
        print ' CCS2 Local Search              Minimum %6i %21.4f' \
              % (taskidx + 1, ene)
        print

        for newmol, newene in self.findneighbor(mol):
            if self.isuseful(newene):
                self.addtask(newmol, newene)
            if newene < self.lowestene:
                self.lowestene = newene
                if ene >= self.searchbound:
                    return

    def isuseful(self, ene):
        if not self.isnewene(ene):
            return False
        if self.keeprange is None or self.searchrange is None:
            return True
        if ene <= self.keepbound or ene <= self.searchbound:
            return True
        return False

    def addtask(self, mol, ene):
        self.tasks.append((mol, ene))
        taskidx = len(self.tasks) - 1
        heapq.heappush(self.taskheap, (ene, taskidx))
        bisect.insort(self.enes, ene)
        print
        print '    Potential Surface Map       Minimum ' \
              '%6i %21.4f' % (taskidx+1, ene)
        print
        self.writemol(taskidx+1, mol, ene)

    def taskqueue(self):
        while self.taskheap:
            ene, taskidx = heapq.heappop(self.taskheap)
            if self.searchbound is not None and ene > self.searchbound:
                print self.searchbound
                return
            yield taskidx

    def getloopatoms(self, mol):
        loops = loopdetect.loopdetect(mol)
        assert len(loops) == 1
        return loops[0]

    def printparams(self):
        print 'Starttime: %s' % time.asctime()
        print 'Forcefield: %s' % self.forcefield
        print 'KeepRange: %s' % self.keeprange
        print 'SearchRange: %s' % self.searchrange
        print

    def writemol(self, idx, mol, ene):
        ofname = self.molnametmp % idx
        ofile = file(ofname, 'w+')
        write.writexyz(mol, ofile, '%.4f' % ene)
        ofile.close()

    def isnewene(self, ene):
        idx = bisect.bisect(self.enes, ene)
        if idx - 1 >= 0 and \
               abs(self.enes[idx-1] - ene) < self.eneerror:
            return False
        if idx < len(self.enes) and \
               abs(self.enes[idx] - ene) < self.eneerror:
            return False
        bisect.insort(self.enes, ene)
        return True

    def findneighbor(self, mol):
        coords = mol.coords
        dismat = moltools.distmat(mol)
        r6results = {}
        for r6 in self.r6s:
            r6results[r6] = getr6result(coords, r6, dismat, self.shakedata)
        for cmbidx, combine in enumerate(self.combinations):
            r6s = [r6results[r6] for r6 in combine]
            needshakeatoms = []
            for r6 in combine:
                needshakeatoms.extend(R6.R6(r6).needshakenodes())
            result = list(tools.combinecombine(r6s))
            for molidx, molresult in enumerate(result):
                newmol = mol.copy()
                for r6result in molresult:
                    for idx, coord in r6result.items():
                        newmol.coords[idx] = coord
                rmol, rene = tinker.minimizemol(newmol,
                                                self.forcefield,
                                                self.minconverge)
                self.step += 1
                print '  Step %5i   Comb %02i-%02i %42.4f' % \
                      (self.step, cmbidx, molidx, rene)

                yield rmol, rene

    def reorganizeresults(self):
        oldenes = [task[1] for task in self.tasks]
        newenes = oldenes[:]
        newenes.sort()
        if self.keeprange is not None:
            idx = bisect.bisect(newenes, self.keepbound)
            newenes = newenes[:idx]
        print
        print 'Oldidx Newidx Ene(sort by Oldidx)'
        for oldidx, ene in enumerate(oldenes):
            oldfname = self.molnametmp % (oldidx + 1)
            try:
                newidx = newenes.index(ene)
            except ValueError:
                os.unlink(oldfname)
                print '%6i %6s %.4f' % (oldidx+1, '', ene)
            else:
                newfname = self.newmolnametmp % (newidx + 1)
                os.rename(oldfname, newfname)
                print '%6i %6i %.4f' % (oldidx+1, newidx+1, ene)
        print
        print 'Oldidx Newidx Ene(sort by Newidx)'
        for newidx, ene in enumerate(newenes):
            oldidx = oldenes.index(ene)
            print '%6i %6i %.4f' % (oldidx+1, newidx+1, ene)
            
                                          

def getr6result(coords, r6, dismat, shakedata):
    if r6type(r6) == (1,1,1,1,1,1,1):
        idxs = tuple(itertools.chain(*r6))
        return Mezei.R6(coords, idxs, dismat, shakedata)
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
