# -*- coding: utf8 -*-
# $Id$
import pprint
import bisect
import sys
import signal
import math
import time
import heapq
from itcc.Tinker import tinker
from itcc.CCS2.R6combine import R6combine3
from itcc.CCS2.neighbour import NeighbourI
from itcc.CCS2.neighbour import calctor
from itcc.CCS2.tors import TorsSet
from itcc.CCS2 import getshakeHdata
from itcc.CCS2 import loopdetect
from itcc.CCS2.searchresult import SearchResult

__all__ = ['LoopClosure']
__revision__ = '$Rev$'

def handler(signum, frame):
    from itcc.Molecule import write
    
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    lc = _loopclosure
    print
    lc.printsummary()
    for idx, minimal in enumerate(lc.minimals):
        print idx+1, minimal.ene, minimal.opttimes
        write.writexyz(minimal.mol, sys.stdout)
        print
    sys.exit(1)

_loopclosure = None

class LoopClosure(object):
    __slots__ = ['forcefield', 'runned', 'keepbound', 'searchbound',
                 'mol', 'loopatoms', 'R6s', 'combinations',
                 'shakeHdata', 'knownmols', 'minimals', 'tasks',
                 'finishedtask', 'caseboundary', 'lowestene',
                 'maxsteps', 'f_neighbour', 'f_R6combine', 'torsset'] 
    
    def __init__(self, forcefield, keepbound, searchbound):
        global _loopclosure
        
        self.forcefield = forcefield
        self.runned = False
        self.keepbound = keepbound
        self.searchbound = searchbound
        _loopclosure = self
        self.maxsteps = 0
        self.f_neighbour = NeighbourI
        self.f_R6combine = R6combine3
        self.torsset = TorsSet
        
    def __call__(self, mol):
        assert not self.runned

        self.printparams()
        
        mol, ene = tinker.optimizemol(mol, self.forcefield)

        self.loopatoms = self.getloopatoms(mol)
        self.R6s = self.getR6s(self.loopatoms)
        self.printR6s(self.R6s)
        self.combinations = self.getcombinations(self.R6s)
        self.printcombinations(self.combinations)
        tors = calctor(mol.coords, self.loopatoms)
        self.knownmols = self.torsset([tors])
        self.shakeHdata = getshakeHdata(mol)
        sys.stdout.flush()

        signal.signal(signal.SIGTERM, handler)
        signal.signal(signal.SIGINT, handler)

        if self.searchbound is None and self.keepbound is None:
            self.caseboundary = self.noboundary
        elif self.searchbound is not None and self.keepbound is not None:
            self.caseboundary = self.boundary
        else:
            assert False

        self._run(mol, ene)

            
        print 'We got %i conformations' % len(self.minimals)
        print
        self.runned = True
        self.printsummary()
        return self.minimals

    def _run(self, mol, ene):
        self.tasks = [self.f_neighbour(mol, ene, self)]
        self.minimals = [SearchResult(mol, ene, tinker.minimize_count)]
        minimals = self.minimals
        self.lowestene = ene
        self.finishedtask = 0

        starttime = time.time()
        
        while True:
            try:
                newmol, newene = self.tasks[0].next()
            except StopIteration:
                self.finishedtask += 1
                heapq.heappop(self.tasks)
                if not self.tasks:
                    break
                continue
            heapq.heapreplace(self.tasks, self.tasks[0])
            
            if newmol is not None:
                self.caseboundary(newmol, newene)

            if tinker.minimize_count % 10 == 0:
                self.printsmallsummary()
                if tinker.minimize_count % 100 == 0:
                    self.printenes()
                    endtime = time.time()
                    print 'Time: %.2f' % (endtime - starttime)
                    sys.stdout.flush()
                    starttime = endtime

            if self.maxsteps and tinker.minimize_count >= self.maxsteps:
                break
        return minimals

    def noboundary(self, newmol, newene):
        if tinker.isminimal(newmol, self.forcefield):
            newresult = SearchResult(newmol, newene, tinker.minimize_count)
            bisect.insort(self.minimals, newresult)
            heapq.heappush(self.tasks, self.f_neighbour(newmol, newene, self))
            if newene < self.lowestene:
                self.lowestene = newene

    def boundary(self, newmol, newene):
        lowestene = self.lowestene
        searchbound = self.searchbound
        keepbound = self.keepbound
        
        if lowestene < newene < lowestene + max(searchbound, keepbound):
            if not tinker.isminimal(newmol, self.forcefield):
                return
        if newene < lowestene:
            self.lowestene = newene
            del self.minimals[bisect.bisect(self.minimals, newene+keepbound):]
            self.tasks = [task for task in self.tasks
                          if task.ene <= newene + searchbound]
            heapq.heapify(self.tasks)
        if newene <= lowestene + searchbound:
            heapq.heappush(self.tasks, self.f_neighbour(newmol, newene, self))
        if newene <= lowestene + keepbound:
            newresult = SearchResult(newmol, newene, tinker.minimize_count)
            bisect.insort(self.minimals, newresult)

    def getloopatoms(self, mol):
        loops = loopdetect(mol)
        assert len(loops) == 1
        return loops[0]
        
    def getR6s(self, loopatoms):
        doubleloop = loopatoms * 2
        return [tuple(doubleloop[i:i+7]) for i in range(len(loopatoms))]

    def printR6s(self, R6s):
        print "This loop has %i R6 blocks:" % len(R6s)
        pprint.pprint(R6s)
        print

    def getcombinations(self, R6s):
        return R6combine3(R6s)

    def printcombinations(self, combinations):
        print "These R6 blocks have %i kinds of combination:" % len(combinations)
        for i, combination in enumerate(combinations):
            print "Combination-%i: %s" % (i, combination)
        print

    def getprogress(self):
        totaltask = self.finishedtask + len(self.tasks)
        finishedtask = float(self.finishedtask)
        for task in self.tasks:
            finishedtask += task.getprogress()
        return finishedtask/totaltask

    def printparams(self):
        print 'Forcefield: %s' % self.forcefield
        print 'KeepBound: %s' % self.keepbound
        print 'SearchBound: %s' % self.searchbound
        print 'Neigbout Algorithm: %s' % self.f_neighbour.idstr
        print

    def printsmallsummary(self):
        minimals = self.minimals
        print 'Min %i, Good %i, Energy:%.4f-%.4f, %.1f%%' % \
              (tinker.minimize_count, len(minimals),
               minimals[0].ene, minimals[-1].ene, 100*self.getprogress())
        sys.stdout.flush()

    def printsummary(self):
        print 'Total optimization times: %i' % tinker.minimize_count
        print '  Find the best minimal at: %i' % self.minimals[0].opttimes
        print '  Find first minimal at: %i' % min([x.opttimes for x in
                                                   self.minimals]) 
        print '  Find last minimal at: %i' % max([x.opttimes for x in
                                                  self.minimals]) 
        print '  Wasted optimization times: %i' % \
              (tinker.minimize_count - max([x.opttimes for x in
                                            self.minimals])) 
        print '  The largest minimal find times gap: %i' % self.getmintimesgap()
        print
        self.printenes()
        self.printtors()
        
    def getmintimesgap(self):
        times = [x.opttimes for x in self.minimals]
        times.sort()
        timesgap = [times[i+1] - times[i] for i in range(len(times)-1)]
        if not timesgap:
            return 0
        else:
            return max(timesgap)

    def printenes(self):
        minimals = self.minimals
        enes = [minimal.ene for minimal in minimals]
        for i in range(0, len(enes), 5):
            print ' '.join(['%.4f' % ene for ene in enes[i:i+5]])
        print
        sys.stdout.flush()

    def printtors(self):
        doubleloop = self.loopatoms * 2
        for idx, minimal in enumerate(self.minimals):
            tors = [math.degrees(minimal.mol.calctor(*doubleloop[i:i+4]))
                    for i in range(len(self.loopatoms))]
            
            print idx+1,
            print '['+', '.join(['%.1f' % tor for tor in tors])+']'
        print
