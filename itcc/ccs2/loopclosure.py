# $Id$
import os
import os.path
import math
import bisect
import heapq
import sets
import pprint
import itertools
import time
from itcc.tinker import tinker
from itcc.molecule import read, write, tools as moltools
from itcc.tools import tools
from itcc.ccs2 import loopdetect, base, peptide, catordiff, sidechain
from itcc.ccs2 import mezeipro2
from itcc.ccs2 import r6 as R6
from itcc.ccs2 import mezei as Mezei
from itcc.ccs2 import mezeipro as Mezeipro

__all__ = ['LoopClosure']
__revision__ = '$Rev$'

class LoopClosure:
    def __init__(self, forcefield, keeprange, searchrange):
        self.forcefield = forcefield
        self.keeprange = keeprange
        self.searchrange = searchrange
        self.maxsteps = None
        self.eneerror = 0.0001          # unit: kcal/mol
        self.torerror = 10              # unit: degree
        self.moltypekey = None
        self.tasks = []                 # List of (mol, ene)
        self.taskheap = []              # Heap of (ene, taskidx)
        self.enes = []                  # Sorted List of (ene, taskidx)
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
        if self.loopatoms is None:
            print "this moleclue does not contain loop. exit."
            return
        if len(self.loopatoms) < 6:
            print "your ring is %s-member, we can't deal with ring less than 6-member." % len(self.loopatoms)
            return
        self.shakedata = getshakedata(mol, self.loopatoms)
        self.r6s = tuple(typedmol.getr6s(self.loopatoms))
        printr6s(self.r6s)
        self.combinations = tuple(typedmol.getcombinations(self.r6s))
        self.r6s = tuple(sets.Set(itertools.chain(*self.combinations)))
        printcombinations(self.combinations)

        mol, ene = tinker.minimizemol(mol, self.forcefield, self.minconverge)
        self.lowestene = ene
        self.addtask(mol, ene)
        for taskidx in self.taskqueue():
            self.runtask(taskidx)
        self.reorganizeresults()
        self.printend()

    def runtask(self, taskidx):
        mol, ene = self.tasks[taskidx]
        print
        head = ' CCS2 Local Search(%i/%i)' % self.getprogress()
        print '%-31s Minimum %6i %21.4f' \
              % (head, taskidx + 1, ene)
        print

        for newmol, newene in self.findneighbor(mol):
            idx = self.eneidx(newmol, newene)
            if idx >= 0:
                print '(%i)' % (idx + 1)
            else:
                print
            if idx == -1:
                self.addtask(newmol, newene)
            if newene < self.lowestene:
                self.lowestene = newene
                if self.searchbound is not None and ene >= self.searchbound:
                    return

    def eneidx(self, mol, ene):
        '''return the taskidx, if is new ene, return -1, if is out of range, return -2'''
        if self.keeprange is not None and \
           self.searchrange is not None:
            if ene > max(self.keepbound, self.searchbound):
                return -2

        initidx = bisect.bisect(self.enes, (ene,))
        for idx in range(initidx-1, -1, -1):
            ene2 = self.enes[idx][0]
            if round(ene - ene2, 4) > self.eneerror:
                break
            taskidx = self.enes[idx][1]
            mol2 = self.tasks[taskidx][0]
            if catordiff.catordiff(mol, mol2) <= math.radians(self.torerror):
                return taskidx
        for idx in range(initidx, len(self.enes)):
            ene2 = self.enes[idx][0]
            if round(ene2 - ene, 4) > self.eneerror:
                break
            taskidx = self.enes[idx][1]
            mol2 = self.tasks[taskidx][0]
            if catordiff.catordiff(mol, mol2) <= math.radians(self.torerror):
                return taskidx
        return -1

    def addtask(self, mol, ene):
        self.tasks.append((mol, ene))
        taskidx = len(self.tasks) - 1
        heapq.heappush(self.taskheap, (ene, taskidx))
        bisect.insort(self.enes, (ene, taskidx))
        print '    Potential Surface Map       Minimum ' \
              '%6i %21.4f' % (taskidx+1, ene)
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
        if loops:
            assert len(loops) == 1
            return loops[0]
        else:
            return None

    def printparams(self):
        print 'Starttime: %s' % time.asctime()
        print 'Forcefield: %s' % self.forcefield
        print 'KeepRange: %s' % self.keeprange
        print 'SearchRange: %s' % self.searchrange
        print

    def printend(self):
        print 'Endtime: %s' % time.asctime()
        try:
            import resource
        except ImportError:
            pass
        else:
            res = resource.getrusage(resource.RUSAGE_CHILDREN)
            print 'Time used by external program: %.1fs(%.1f+%.1f)' % (res[0]+res[1], res[0], res[1])
            res = resource.getrusage(resource.RUSAGE_SELF)
            print 'Time used by   this   program: %.1fs(%.1f+%.1f)' % (res[0]+res[1], res[0], res[1])

    def writemol(self, idx, mol, ene):
        ofname = self.molnametmp % idx
        ofile = file(ofname, 'w+')
        write.writexyz(mol, ofile, '%.4f' % ene)
        ofile.close()

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
                if tinker.isminimal(rmol, self.forcefield):
                    print '  Step %5i   Comb %02i-%02i %42.4f' % \
                          (self.step, cmbidx, molidx, rene),
                    yield rmol, rene
                else:
                    print '  Step %5i   Comb %02i-%02i Not a minimum %28.4f' % \
                          (self.step, cmbidx, molidx, rene)

    def reorganizeresults(self):
        if self.keeprange is None:
            newidxs = [ene[1] for ene in self.enes]
        else:
            newidxs = [ene[1] for ene in self.enes if ene[0] <= self.keepbound]

        print
        print 'Oldidx Newidx Ene(sort by Oldidx)'
        for oldidx in range(len(self.tasks)):
            ene = self.tasks[oldidx][1]
            oldfname = self.molnametmp % (oldidx + 1)
            try:
                newidx = newidxs.index(oldidx)
            except ValueError:
                os.unlink(oldfname)
                print '%6i %6s %.4f' % (oldidx+1, '', ene)
            else:
                newfname = self.newmolnametmp % (newidx + 1)
                os.rename(oldfname, newfname)
                print '%6i %6i %.4f' % (oldidx+1, newidx+1, ene)

        print
        print 'Oldidx Newidx Ene(sort by Newidx)'
        for newidx, oldidx in enumerate(newidxs):
            print '%6i %6i %.4f' % (oldidx+1, newidx+1, self.tasks[oldidx][1])
        print

    def getprogress(self):
        finishedtasknum = len(self.tasks) - len(self.taskheap)
        if self.searchrange is None:
            waitingtasknum = len(self.taskheap)
        else:
            waitingtasknum = 0
            searchbound = self.searchbound
            for ene, _ in self.taskheap:
                if ene <= searchbound:
                    waitingtasknum += 1
        return finishedtasknum, waitingtasknum

def getr6result(coords, r6, dismat, shakedata):
    type_ = r6type(r6)
    if type_ == (1, 1, 1, 1, 1, 1, 1):
        idxs = tuple(itertools.chain(*r6))
        return Mezei.R6(coords, idxs, dismat, shakedata)
    elif type_ == (2, 1, 2, 1, 2, 1, 2):
        idxs = tuple(itertools.chain(*r6))[1:-1]
        return Mezeipro.R6(coords, idxs, dismat, shakedata)
    elif type_ == (1, 2, 1, 2, 1, 2, 1):
        idxs = tuple(itertools.chain(*r6))
        return mezeipro2.R6(coords, idxs, dismat, shakedata)
    assert False, r6type(r6)

def r6type(r6):
    return tuple([len(x) for x in r6])

moltypedict = {'peptide': peptide.Peptide}
def getmoltype(key):
    return moltypedict.get(key, base.Base)

def getshakedata(mol, loop):
    result = {}
    dloop = loop * 2
    for idx, atomidx in enumerate(loop):
        refidxs = [atomidx, dloop[idx-1], dloop[idx+1]]
        sidechain_ = sidechain.getsidechain(mol, loop, atomidx)
        result[atomidx] = (refidxs, sidechain_)
    return result

def printr6s(r6s):
    print "This loop has %i R6 blocks:" % len(r6s)
    pprint.pprint(r6s)
    print

def printcombinations(combinations):
    print "These R6 blocks have %i kinds of combination:" % len(combinations)
    for i, combination in enumerate(combinations):
        print "Combination-%i: %s" % (i, combination)
    print
