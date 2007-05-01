# $Id$
import sys
import os
import os.path
import math
import bisect
import heapq
import pprint
import itertools
import time
import random
import tempfile
import shutil
import cPickle
try:
    import threading
except ImportError:
    import dummy_threading as threading

import itcc
from itcc.tinker import tinker
from itcc.molecule import read, write, mtxyz, chiral, tools as moltools
from itcc.ccs2 import detectloop, base, peptide, catordiff, sidechain
from itcc.ccs2 import mezeipro2
from itcc.ccs2 import mezei as Mezei
from itcc.ccs2 import mezeipro as Mezeipro

__all__ = ['LoopClosure']
__revision__ = '$Rev$'

class LoopClosure(object):
    # in some forcefield (e.g. OPLSAA), there some illegal structure
    # with extremely low energy (e.g. -13960945.7658 kcal/mol), so we
    # treat all structure with energy lower than self.legal_min_ene is
    # illegal.
    legal_min_ene = -100000

    S_NONE = 0
    S_INITED = 1

    def __init__(self):
        self.forcefield = None
        self.keeprange = None
        self.searchrange = None
        self.maxsteps = None
        self.eneerror = 0.0001          # unit: kcal/mol
        self.torerror = 10              # unit: degree
        self.minconverge = 0.001
        self.moltypekey = None
        self.loop = None

        self._step_count = 0
        self.seedmol = None
        self._tasks = []                # List of (coords, ene)
        self.taskheap = []              # Heap of (r6idx, ene, taskidx, r6)
        self.enes = []                  # Sorted List of (ene, taskidx)
        self.tmp_mtxyz_fname = None
        self.tmp_mtxyz_file = None
        self.newmolnametmp = None
        self.lowestene = None
        self.shakedata = None
        self.start_time = None
        self.olddir = None
        self.newdir = None
        self.log_level = 1
        self.state = self.S_NONE

        self.check_minimal = True
        self.check_chiral = False
        self.chiral_idxs = []
        self._chirals = []
        self.dump_steps = 100

        self.np = 1
        self.multithread = False
        self.mutex = threading.Lock()
        self.solvate = None

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['tmp_mtxyz_file']
        del odict['mutex']
        return odict

    def __setstate__(self, dict):
        self.__dict__.update(dict)
        self.olddir = os.getcwd()
        self.newdir = tempfile.mkdtemp('itcc')
        os.chdir(self.newdir)
        if self.tmp_mtxyz_fname is not None:
            self.tmp_mtxyz_fname = \
                os.path.join(self.olddir,
                             os.path.basename(self.tmp_mtxyz_fname))
            self.tmp_mtxyz_file = file(self.tmp_mtxyz_fname, 'ab+')
            for i in range(len(self._tasks)):
                read.readxyz(self.tmp_mtxyz_file)
            self.tmp_mtxyz_file.truncate()
        else:
            self.tmp_mtxyz_file = None
        self.mutex = threading.Lock()

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

    def __call__(self, molfile):
        assert self.forcefield is not None
        if not self._prepare(molfile):
            return

        if self.np > 1:
            self._run_multi_thread()
        else:
            self._run_single_thread()

    def _run_single_thread(self):
        self.multithread = False
        last_dump_step = self._step_count
        while self.maxsteps is None \
              or self._step_count < self.maxsteps:
            if self._step_count - last_dump_step >= self.dump_steps:
                self.dump()
                last_dump_step = self._step_count
                os.system("ps -p %s -o rss" % os.getpid())
            try:
                taskidx, r6 = self.taskqueue().next()
            except StopIteration:
                break
            self.runtask(taskidx, r6)
        self._cleanup()

    def _run_multi_thread(self):
        self.multithread = True

        threads = []
        last_dump_step = self._step_count

        def clear_threads():
            threads[:] = [x for x in threads if x.isAlive()]

        some_threads_finished_condition = \
            threading.Condition(self.mutex, verbose=True)

        class Task:
            def __init__(self, parent, taskidx, r6):
                self.parent = parent
                self.taskidx = taskidx
                self.r6 = r6
            def __call__(self):
                self.parent.runtask(self.taskidx, self.r6) 
                self.parent.mutex.acquire()
                some_threads_finished_condition.notify()
                self.parent.mutex.release()

        while True:
            some_threads_finished_condition.acquire()
            clear_threads()
            if (not threads and not self.taskheap) \
              or (self.maxsteps is not None
                  and self._step_count >= self.maxsteps) :
                some_threads_finished_condition.release()
                for thread in threads:
                    thread.join()
                break
            if self._step_count - last_dump_step >= self.dump_steps:
                some_threads_finished_condition.release()
                for thread in threads:
                    thread.join()
                self.dump()
                last_dump_step = self._step_count
                continue

            need_wait = False
            while len(threads) < self.np and self.taskheap:
                r6idx, ene, taskidx, r6 = heapq.heappop(self.taskheap)
                if self.searchbound is not None and ene > self.searchbound:
                    continue
                task = Task(self, taskidx, r6)
                thread = threading.Thread(target = task, verbose = True)
                threads.append(thread)
                thread.start()
                need_wait = True

            if need_wait:
                some_threads_finished_condition.wait()

            some_threads_finished_condition.release()
        self._cleanup()

    def dump(self):
        self.tmp_mtxyz_file.flush()
        ofname = os.path.join(self.olddir, 'checkfile.part')
        ofile = file(ofname, 'w')
        cPickle.dump(self, ofile, 1)
        ofile.close()

        os.rename(ofname, os.path.join(self.olddir, 'checkfile'))

    def _get_tinker_key(self):
        res = 'ENFORCE-CHIRALITY\n'
        if self.solvate is not None:
            res += 'SOLVATE %s\n' % self.solvate
        return res
        
        
    def _prepare(self, molfile):
        if self.state != self.S_NONE:
            return True
        self.printparams()
        mol = read.readxyz(molfile)
        self.seedmol = mol

        if self.check_chiral:
            self._init_chiral(mol)

        self.olddir = os.getcwd()
        self.newdir = tempfile.mkdtemp('itcc')
        os.chdir(self.newdir)

        file('tinker.key', 'w').write(self._get_tinker_key())
        tinker.curdir = True

        self.newmolnametmp = os.path.splitext(molfile.name)[0] + '.%03i'
        fd, self.tmp_mtxyz_fname = tempfile.mkstemp(dir=self.olddir)
        self.tmp_mtxyz_file = os.fdopen(fd, 'wb+')
        typedmol = getmoltype(self.moltypekey)(mol)
        self.loopatoms = self.getloopatoms(mol)
        if self.loopatoms is None:
            print "this moleclue does not contain loop. exit."
            return False
        if len(self.loopatoms) < 6:
            print "your ring is %s-member, " \
                "we can't deal with ring less than 6-member." \
                % len(self.loopatoms)
            return False
        self.shakedata = getshakedata(mol, self.loopatoms)
        r6s = tuple(typedmol.getr6s(self.loopatoms))
        self.r6s = {}
        for idx, x in enumerate(r6s):
            self.r6s[x] = idx
        printr6s(r6s)

        mol, ene = tinker.minimizemol(mol, self.forcefield, self.minconverge)
        self._step_count += 1
        self.lowestene = ene
        self.addtask(mol, ene)
        self.state = self.S_INITED
        return True

    def _init_chiral(self, mol):
        self._chirals = tuple(chiral.chiral_types(mol, self.chiral_idxs))

    def _cleanup(self):
        os.chdir(self.olddir)
        shutil.rmtree(self.newdir)
        self.reorganizeresults()
        self.printend()

    def runtask(self, taskidx, r6):
        self.mutex.acquire() # r self.tasks
        ene = self._tasks[taskidx][1]
        mol = self.seedmol.copy()
        mol.coords[:] = self._tasks[taskidx][0]
        self.mutex.release()
        print
        head = ' CCS2 Local Search'
        print '%-31s Minimum %6i %21.4f' \
              % (head, taskidx + 1, ene)
        print

        for newmol, newene in self.findneighbor(mol, r6):
            if not self.is_valid(newmol, newene):
                print
                continue
            idx = self.eneidx(newmol, newene)
            if idx >= 0:
                print '(%i)' % (idx + 1)
            else:
                print
            if idx == -1:
                self.addtask(newmol, newene)
            if newene < self.lowestene:
                self.mutex.acquire()
                self.lowestene = newene
                finished = self.searchbound is not None \
                    and ene >= self.searchbound
                self.mutex.release()
                if finished:
                    return

    def eneidx(self, mol, ene):
        '''return the taskidx
        if is new ene, return -1,
        if is out of range, return -2'''
        res = None
        self.mutex.acquire()
        if self.keeprange is not None and \
           self.searchrange is not None:
            if ene > max(self.keepbound, self.searchbound):
                res = -2

        if res is None:
            initidx = bisect.bisect(self.enes, (ene,))
            for idx in range(initidx-1, -1, -1):
                ene2 = self.enes[idx][0]
                if round(ene - ene2, 4) > self.eneerror:
                    break
                taskidx = self.enes[idx][1]
                coords2 = self._tasks[taskidx][0]
                mol2 = self.seedmol.copy()
                mol2.coords[:] = coords2
                if catordiff.catordiff(mol, mol2, self.loop) \
                        <= math.radians(self.torerror):
                    res = taskidx

        if res is None:                
            for idx in range(initidx, len(self.enes)):
                ene2 = self.enes[idx][0]
                if round(ene2 - ene, 4) > self.eneerror:
                    break
                taskidx = self.enes[idx][1]
                coords2 = self._tasks[taskidx][0]
                mol2 = self.seedmol.copy()
                mol2.coords[:] = coords2
                if catordiff.catordiff(mol, mol2, self.loop) \
                        <= math.radians(self.torerror):
                    res = taskidx

        if res is None:
            res = -1
        self.mutex.release()
        return res

    def addtask(self, mol, ene):
        self.mutex.acquire()
        self._tasks.append((mol.coords, ene))
        taskidx = len(self._tasks) - 1
        bisect.insort(self.enes, (ene, taskidx))
        print '    Potential Surface Map       Minimum ' \
              '%6i %21.4f' % (taskidx+1, ene)
        self.writemol(mol, ene)

        r6s = self.r6s.keys()
        random.shuffle(r6s)
        for r6idx, r6 in enumerate(r6s):
            heapq.heappush(self.taskheap, (r6idx, ene, taskidx, r6))
        self.mutex.release()

    def taskqueue(self):
        while self.taskheap:
            r6idx, ene, taskidx, r6 = heapq.heappop(self.taskheap)
            if self.searchbound is not None and ene > self.searchbound:
                continue
            yield taskidx, r6

    def getloopatoms(self, mol):
        if self.loop is not None:
            for i in range(len(self.loop)):
                assert mol.is_connect(self.loop[i], self.loop[i-1])
            return self.loop

        looptype, loops = detectloop.loopdetect(mol)
        if looptype == detectloop.SIMPLELOOPS \
           and len(loops) == 1:
            self.loop = loops[0]
        return self.loop

    def printparams(self):
        self.start_time = time.time()
        print 'Starttime: %s' % time.ctime(self.start_time)
        print 'Program Version: itcc %s' %  itcc.__version__
        print 'Forcefield: %s' % tinker.getparam(self.forcefield)
        print 'KeepRange: %s' % self.keeprange
        print 'SearchRange: %s' % self.searchrange
        print 'MaxSteps: %s' % self.maxsteps
        print 'MolType: %s' % self.moltypekey
        if self.loop is None:
            print 'Loop: auto'
        else:
            print 'Loop: %s' % ' '.join(str(x+1) for x in self.loop)

        if not self.check_chiral:
            print 'Chiral: none'
        else:
            print 'Chiral: %s' % ' '.join(str(x+1) for x in self.chiral_idxs)
        print

    def printend(self):
        import datetime

        print 'Starttime: %s' % time.ctime(self.start_time)
        end_time = time.time()
        print 'Endtime: %s' % time.asctime()
        print 'Total time: %s' \
            % datetime.timedelta(0, end_time - self.start_time)

        try:
            import resource
        except ImportError:
            pass
        else:
            res_c = resource.getrusage(resource.RUSAGE_CHILDREN)
            res_s = resource.getrusage(resource.RUSAGE_SELF)
            res_c_t = res_c[0] + res_c[1]
            res_s_t = res_s[0] + res_s[1]
            res_t = res_c_t + res_s_t
            print 'Total CPU time: %s' % datetime.timedelta(0, res_t)
            print 'Time used by   this   program: %.1fs(%.1f+%.1f)' \
                % (res_s_t, res_s[0], res_s[1])
            print 'Time used by external program: %.1fs(%.1f+%.1f)' \
                % (res_c_t, res_c[0], res_c[1])

    def writemol(self, mol, ene):
        write.writexyz(mol, self.tmp_mtxyz_file, '%.4f' % ene)

    def findneighbor(self, mol, r6):
        coords = mol.coords
        dismat = moltools.distmat(mol)
        for molidx, molresult \
                in enumerate(getr6result(coords, r6, dismat, self.shakedata)):
            newmol = mol.copy()
            for idx, coord in molresult.items():
                newmol.coords[idx] = coord
            rmol, rene = \
                tinker.minimizemol(newmol,
                                   self.forcefield,
                                   self.minconverge,
                                   prefix=threading.currentThread().getName())
            self.mutex.acquire() # r/w _step_count
            self._step_count += 1
            self.log('  Step %5i   Comb %02i-%02i %42.4f '
                       % (self._step_count, self.r6s[r6], molidx, rene), 
                     1)
            self.mutex.release()
            yield rmol, rene
            if self.maxsteps is not None and self._step_count >= self.maxsteps:
                return

    def reorganizeresults(self):
        self.tmp_mtxyz_file.seek(0)
        oldmols = mtxyz.Mtxyz(self.tmp_mtxyz_file)

        if self.keeprange is None:
            newidxs = [ene[1] for ene in self.enes]
        else:
            newidxs = [ene[1] for ene in self.enes if ene[0] <= self.keepbound]

        print
        print 'Oldidx Newidx Ene(sort by Oldidx)'
        for oldidx, oldmol in enumerate(oldmols.read_mol_as_string()):
            ene = self._tasks[oldidx][1]
            try:
                newidx = newidxs.index(oldidx)
            except ValueError:
                print '%6i %6s %.4f' % (oldidx+1, '', ene)
            else:
                newfname = self.newmolnametmp % (newidx + 1)
                file(newfname, 'w').write(oldmol)
                print '%6i %6i %.4f' % (oldidx+1, newidx+1, ene)

        print
        print 'Oldidx Newidx Ene(sort by Newidx)'
        for newidx, oldidx in enumerate(newidxs):
            print '%6i %6i %.4f' % (oldidx+1, newidx+1, self._tasks[oldidx][1])
        print

    def log(self, str, lvl):
        if lvl <= self.log_level:
            sys.stdout.write(str)

    def is_valid(self, mol, ene):
        if ene < self.legal_min_ene:
            return False
        if self.check_chiral \
                and tuple(chiral.chiral_types(mol, self.chiral_idxs)) \
                != self._chirals:
            return False
        if self.check_minimal and not tinker.isminimal(mol, self.forcefield):
            return False
        return True

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

_moltypedict = {'peptide': peptide.Peptide}
def getmoltype(key):
    return _moltypedict.get(key, base.Base)

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
    sys.stdout.flush()

def printcombinations(combinations):
    print "These R6 blocks have %i kinds of combination:" % len(combinations)
    for i, combination in enumerate(combinations):
        print "Combination-%i: %s" % (i, combination)
    print
