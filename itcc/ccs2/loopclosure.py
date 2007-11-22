# $Id$
# pylint: disable-msg=E1101
# pylint: disable-msg=W0201
import math
import sys
import os
import os.path
import bisect
import heapq
import pprint
import time
import random
import tempfile
import shutil
import cPickle
import logging
import socket
from cStringIO import StringIO
try:
    import threading
except ImportError:
    import dummy_threading as threading

import itcc
from itcc.tinker import tinker
from itcc.molecule import read, write, mtxyz, chiral, tools as moltools
from itcc.ccs2 import detectloop, base, peptide, sidechain
from itcc.ccs2 import mezeipro2, tordiff
from itcc.ccs2 import mezei as Mezei
from itcc.ccs2 import mezeipro as Mezeipro

__all__ = ['LoopClosure']
__revision__ = '$Rev$'

class Error(Exception):
    pass

class LoopClosure(object):
    '''need a doc'''
    S_NONE = 0
    S_INITED = 1
    
    config_keys = {
        'DEFAULT': (('moltypekey', str, ""),
                    ('cmptorsfile', str, ""),
                    ('loopfile', str, ""),
                    ('chiral_index_file', str, ""),
                    ('molfname', str, ""),
                    ('is_chain', bool, False),
                    ('log_iter', bool, False),
                    ('check_energy_before_minimization', bool, True),
                    ('is_achiral', str, "auto"),
                    ('check_minimal', bool, False),
                    ('out_mtxyz', bool, True),
                    ('out_mtxyz_fname', str, "%(molfname)s-out"),
                    ('maxsteps', int, -1),
                    ('dump_steps', int, 1000),
                    ('np', int, 1),
                    ('head_tail', str, "auto"),
                    ('loopstep', str, "auto"),
                    ('log_level', int, 1),
                    ('keeprange', float, -1.0),
                    ('searchrange', float, -1.0),
                    ('eneerror', float, 0.00015),
                    ('legal_min_ene', float, -100000),
                    ('torerror', float, 10.0),
                    ('minimal_invalid_energy_before_minimization', float, 100000.0),
                    ('min_method', str, 'newton'),
                    ),
        'tinker': (('forcefield', str, "mm2"),
                   ('solvate', str, ""),
                   ('tinker_key_file', str, ""),
                   ('minconverge', float, 0.001))
        }
    
    def get_default_config(cls):
        from ConfigParser import ConfigParser
        res = ConfigParser()
        for sect, val in cls.config_keys.items():
            if sect != 'DEFAULT':
                res.add_section(sect)
            for x in val:
                res.set(sect, x[0], str(x[2]))
        return res
    get_default_config = classmethod(get_default_config)

#        defaults = {
#                'log_level': '1',
#                'np': '1',
#                # molecule type
#                'forcefield': 'mm2',
#
#                # loop type
#                'is_chain': 'False',
#
#                # dump
#                'dump_steps': '100',
#
#                # before minimization
#                'check_energy_before_minimization': 'True',
#                'minimal_invalid_energy_before_minimization': '100000', # unit: kcal/mol
#
#                # minimization
#                # 'minimization_method': 'newton',
#                'minconverge': '0.001', # unit: ?
#                # 'tinker_keep_chiral': 'true',
#
#                # after minimization
#                'legal_min_ene': '-100000', # unit: kcal/mol
#                'check_minimal': 'False',
#
#                # check
#                'eneerror': '0.0001', # unit: kcal/mol
#                'torerror': '10',     # unit: degree
#                }
                
    def __init__(self, config):
        self.config = config

        methods = {str: self.config.get,
                   bool: self.config.getboolean,
                   int: self.config.getint,
                   float: self.config.getfloat}
        for sect, val in self.config_keys.items():
            for x in val:
                setattr(self, x[0], methods[x[1]](sect, x[0]))

        self.cmptors = None
        self.torerror_radian = math.radians(self.torerror)

        self._step_count = 0
        self.seedmol = None
        self._tasks = []                # List of (coords, ene)
        self.taskheap = []              # Heap of (r6idx, ene, taskidx, r6)
        self.enes = []                  # Sorted List of (ene, taskidx)
        self.tmp_mtxyz_fname = None
        self.tmp_mtxyz_file = None
        self.lowestene = None
        self.shakedata = None
        self.start_time = None
        self.olddir = None
        self.newdir = None
        self.state = self.S_NONE

        self.chiral_idxs = None
        self._chirals = []

        self.multithread = False
        self.mutex = threading.Lock()
        self.loopatoms = None
        self.r6s = None

        min_func_dict = {'newton': tinker.newton_mol,
                         'minimize': tinker.minimize_mol,
                         'optimize': tinker.optimize_mol}
        if self.config.getboolean('DEFAULT', 'log_iter'):
            self.min_algo = tinker.NewtonMol(log_iter=True)
            min_func_dict['newton'] = self.min_algo.newton_mol

        if self.min_method not in min_func_dict:
            raise Error("unknown min_method `" + self.min_method + "'")
        self.min_func = min_func_dict[self.min_method]
        

    def run(self):
        logging.getLogger().setLevel(logging.INFO)
        logging.debug('enter run')
        logging.debug('call self.init')
        if not self.init():
            return
        logging.debug('return from self.init')

        if self.np > 1:
            self._run_multi_thread()
        else:
            self._run_single_thread()

    __call__ = run

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['tmp_mtxyz_file']
        del odict['mutex']
        return odict

    def __setstate__(self, dicts):
        self.__dict__.update(dicts)
        self.olddir = os.getcwd()
        self.newdir = tempfile.mkdtemp('itcc')
        os.chdir(self.newdir)
        if self.tmp_mtxyz_fname is not None:
            self.tmp_mtxyz_fname = \
                os.path.join(self.olddir,
                             os.path.basename(self.tmp_mtxyz_fname))
            self.tmp_mtxyz_file = file(self.tmp_mtxyz_fname, 'ab+')
            for i in range(len(self._tasks)): #pylint: disable-msg=W0612
                read.readxyz(self.tmp_mtxyz_file)
            self.tmp_mtxyz_file.truncate()
        else:
            self.tmp_mtxyz_file = None
        self.mutex = threading.Lock()

    def getkeepbound(self):
        if self.keeprange < 0:
            return None
        return self.lowestene + self.keeprange
    keepbound = property(getkeepbound)

    def getsearchbound(self):
        if self.searchrange < 0:
            return None
        return self.lowestene + self.searchrange
    searchbound = property(getsearchbound)


    def _run_single_thread(self):
        logging.debug('enter _run_single_thread')
        self.multithread = False
        last_dump_step = self._step_count
        while self.maxsteps < 0 \
              or self._step_count < self.maxsteps:
            if self._step_count - last_dump_step >= self.dump_steps:
                self.dump()
                last_dump_step = self._step_count
            try:
                taskidx, r6 = self.taskqueue().next()
            except StopIteration:
                break
            logging.debug('call self.runtask')
            self.runtask(taskidx, r6)
            logging.debug('return from self.runtask')
        logging.debug('call self._cleanup')
        self._cleanup()
        logging.debug('return from self._cleanup')

    def _run_multi_thread(self):
        self.multithread = True

        threads = []
        last_dump_step = self._step_count

        def clear_threads():
            threads[:] = [x for x in threads if x.isAlive()]

        some_threads_finished_condition = \
            threading.Condition(self.mutex)

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
              or (self.maxsteps >= 0
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
                ene, taskidx, r6 = heapq.heappop(self.taskheap)[1:]
                if self.searchbound is not None and ene > self.searchbound:
                    continue
                task = Task(self, taskidx, r6)
                thread = threading.Thread(target = task)
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
        res = ''
        if self.tinker_key_file:
            res += file(os.path.join(self.olddir, self.tinker_key_file)).read()
        if res and res[-1] != '\n':
            res += '\n'
        if not self.is_achiral:
            res += 'ENFORCE-CHIRALITY\n'
        if self.solvate:
            res += 'SOLVATE %s\n' % self.solvate
        return res
        
        
    def init_env(self):
        self.start_time = time.time()
        self.olddir = os.getcwd()
        self.newdir = tempfile.mkdtemp('itcc')
        os.chdir(self.newdir)
        fd, self.tmp_mtxyz_fname = tempfile.mkstemp(dir=self.olddir)
        self.tmp_mtxyz_file = os.fdopen(fd, 'wb+')
        return True

    def init_mol(self):
        self.seedmol = read.readxyz(file(os.path.join(self.olddir,
                                                      self.molfname)))
        return True

    def init_task(self):
        mol, ene = self._minimizemol(self.seedmol)
        if mol is None:
            self.log("weird input molecule\n")
            return False
        self._step_count += 1
        self.lowestene = ene
        self.addtask(mol, ene)
        return True

    def init_loop(self):
        if self.loopatoms is None:
            if self.loopfile:
                self.loopatoms = sum([[int(x) - 1 \
                        for x in line.split()
                        if line.strip() and line[0] != '#']
                        for line in file(os.path.join(self.olddir, self.loopfile)).readlines()], [])
        if self.loopatoms is None:
            loops = detectloop.loopdetect(self.seedmol)
            try:
                self.loopatoms = detectloop.pick_largest_simpleloop(loops)
            except Exception, e:
                self.log(str(e))
                return False

        if len(self.loopatoms) < 6:
            self.log("your ring is %s-member, "
                "we can't deal with ring less than 6-member.\n"
                % len(self.loopatoms))
            return False

        return self._check_loop_atoms(self.seedmol, self.loopatoms)

    def init_r6(self):
        typedmol = getmoltype(self.moltypekey)(self.seedmol)
        r6s = tuple(typedmol.getr6s(self.loopatoms, self.is_chain))
        self.r6s = {}
        for idx, x in enumerate(r6s):
            self.r6s[x] = idx
        return True

    def init_sidechain(self):
        self.shakedata = getshakedata(self.seedmol, self.loopatoms)
        return True

    def init_check(self):
        if self.chiral_idxs is None:
            if self.chiral_index_file:
                self.chiral_idxs = sum([[int(x) - 1 \
                        for x in line.split()
                        if line.strip() and line[0] != '#']
                        for line in file(os.path.join(self.olddir,
			                              self.chiral_index_file)).readlines()], [])

        if self.chiral_idxs:
            self._chirals = tuple(chiral.chiral_types(self.seedmol, self.chiral_idxs))

        if self.head_tail == 'auto':
            if self.moltypekey == 'peptide':
                self.head_tail = -1
            else:
                self.head_tail = 0
        else:
            self.head_tail = int(self.head_tail)
                
            
        if self.is_achiral == "auto":
            if self.moltypekey == 'peptide':
                self.is_achiral = False
            else:
                self.is_achiral = True
        else:
            self.is_achiral = self.config.getboolean('DEFAULT', 'is_achiral')
                
                
        if self.loopstep == "auto":
            if self.moltypekey == 'peptide' or self.is_chain:
                self.loopstep = 0
            else:
                self.loopstep = 1
        else:
            self.loopstep = int(self.loopstep)

        if self.cmptors is None:
            if self.cmptorsfile:
                self.cmptors = [[int(x)-1 for x in line.split()
                    if line.strip() and line[0] != '#']
                    for line in file(self.cmptorsfile).readlines()]

        if self.cmptors is None:
            if self.is_chain:
                self.cmptors = \
                    [self.loopatoms[i:i+4] for i in range(len(self.loopatoms)-3)]
            else:
                self.cmptors = \
                    [(self.loopatoms*2)[i:i+4] for i in range(len(self.loopatoms))]

        for x in self.cmptors:
            assert len(x) == 4
        return True

    def init_tinker(self):
        content = self._get_tinker_key()
        if content:
            file('tinker.key', 'w').write(content)
        tinker.curdir = True
        return True

    def init(self):
        if self.state != self.S_NONE:
            return True

        self.print_copyright()
        self.print_config()
        if not (self.init_env()
                and self.init_mol()
                and self.init_loop()
                and self.init_r6()
                and self.init_sidechain()
                and self.init_check()
                and self.init_tinker()
                and self.init_task()
                ):
            return False
        self.print_params()

        self.state = self.S_INITED
        return True

    def _cleanup(self):
        os.chdir(self.olddir)
        shutil.rmtree(self.newdir)
        logging.debug('call self.reorganizeresults')
        self.reorganizeresults()
        logging.debug('return from self.reorganizeresults')
        self.printend()

    def runtask(self, taskidx, r6):
        self.mutex.acquire() # r self.tasks
        ene = self._tasks[taskidx][1]
        mol = self.seedmol.copy()
        mol.coords = self._tasks[taskidx][0]
        self.mutex.release()
        self.log('\n')
        head = ' CCS2 Local Search'
        self.log('%-31s Minimum %6i %21.4f\n\n'
              % (head, taskidx + 1, ene))

        for newmol, newene, logstr in self.findneighbor(mol, r6):
            validstr = self.is_valid(newmol, newene)
            if validstr != 'V':
                self.log('%s %s\n' % (logstr, validstr))
                continue
            idx = self.eneidx(newmol, newene)
            if idx >= 0:
#                 if newene < self.enes[idx][0]:
#                     self.update_ene_task(idx, newene, newmol.coords)
                self.log(logstr + '(%i)\n' % (idx + 1))
            else:
                self.log(logstr + '\n')
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
    
    def update_ene_task(self, eneidx, newene, newcoord):
        '''sometime we find a duplicate record but with a lower energy,
        we need to replace the archived record with this record'''
        self.mutex.acquire()
        old_rec = self.enes[eneidx]
        del self.enes[eneidx]
        bisect.insort(self.enes, (newene, old_rec[1]))
        taskidx = old_rec[1]
        self._tasks[taskidx] = (newcoord.copy(), newene)
        self._tasks[taskidx][0].setflags(write=False)
        self.mutex.release()

    def eneidx(self, mol, ene):
        '''return the taskidx
        if is new ene, return -1,
        if is out of range, return -2'''
        res = None
        self.mutex.acquire()
        if self.keeprange >= 0 and \
           self.searchrange >= 0:
            if ene > max(self.keepbound, self.searchbound):
                res = -2

        if res is None:
            for idx in range(bisect.bisect_left(self.enes, (ene-self.eneerror,)),
                             bisect.bisect_right(self.enes, (ene+self.eneerror,))):
                ene2 = self.enes[idx][0]
                taskidx = self.enes[idx][1]
                coords2 = self._tasks[taskidx][0]
                mol2 = self.seedmol.copy()
                mol2.coords = coords2
                if self._check_tor(mol, mol2):
                    res = taskidx
                    break

        if res is None:
            res = -1
        self.mutex.release()
        return res

    def addtask(self, mol, ene):
        self.mutex.acquire()
        self._tasks.append((mol.coords.copy(), ene))
        self._tasks[-1][0].setflags(write=False)
        taskidx = len(self._tasks) - 1
        bisect.insort(self.enes, (ene, taskidx))
        self.log('    Potential Surface Map       Minimum '
              '%6i %21.4f\n' % (taskidx+1, ene))
        self.writemol(mol, ene)
        r6s = self.r6s.keys()
        random.shuffle(r6s)
        for r6idx, r6 in enumerate(r6s):
            heapq.heappush(self.taskheap, (r6idx, ene, taskidx, r6))
        self.mutex.release()

    def taskqueue(self):
        while self.taskheap:
            ene, taskidx, r6 = heapq.heappop(self.taskheap)[1:]
            if self.searchbound is not None and ene > self.searchbound:
                continue
            yield taskidx, r6

    # read self.loopfile
    def _check_loop_atoms(self, mol, loop):
        if self.is_chain:
            count = len(loop) - 1
        else:
            count = len(loop)
        for i in range(count):
            next = (i + 1) % len(loop)
            if not mol.is_connect(loop[i], loop[next]):
                return False
        return True

    def print_params(self):
        msg = 'starttime: %s\n' % time.ctime(self.start_time)
        msg += 'loop: %s\n' % ' '.join([str(x+1) for x in self.loopatoms])
        msg += 'head_tail: %s\n' % self.head_tail
        msg += 'is_achiral: %s\n' % self.is_achiral
        msg += 'loopstep: %s\n' % self.loopstep
        msg += 'r6s:\n'
        msg += r6s2str(self.r6s)
        if self.chiral_idxs:
            msg += 'Chiral: %s\n' % ' '.join([str(x+1) for x in self.chiral_idxs])
        msg += 'tinker.key:\n'
        msg += self._get_tinker_key()
        msg += '\n'
        self.log(msg)

    def printend(self):
        import datetime

        if self.config.getboolean('DEFAULT', 'log_iter') and self.min_algo.iters:
            self.log('minimization iterations:\n')
            for i in range(0, len(self.min_algo.iters), 10):
                self.log(''.join(['%4i' % x for x in self.min_algo.iters[i:i+10]])+'\n')
            self.log('\n')

        self.log('Starttime: %s\n' % time.ctime(self.start_time))
        end_time = time.time()
        self.log('Endtime: %s\n' % time.asctime())
        self.log('Total time: %s\n'
                 % datetime.timedelta(0, end_time - self.start_time))

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
            self.log('Total CPU time: %s\n' % datetime.timedelta(0, res_t))
            self.log('Time used by   this   program: %.1fs(%.1f+%.1f)\n'
                     % (res_s_t, res_s[0], res_s[1]))
            self.log('Time used by external program: %.1fs(%.1f+%.1f)\n'
                     % (res_c_t, res_c[0], res_c[1]))

    def writemol(self, mol, ene):
        write.writexyz(mol, self.tmp_mtxyz_file, '%.4f' % ene)

    def findneighbor(self, mol, r6):
        coords = mol.coords
        # FIXME: we need not calculate the full distance matrix
        # FIXME: we need not calculate distmat for each r6
        dismat = moltools.distmat(mol)
        for molidx, molresult \
                in enumerate(getr6result(coords, r6, dismat, self.shakedata)):
            newmol = mol.copy()
            for idx, coord in molresult.items():
                newmol.change_coord(idx, coord)
            rmol, rene = self._minimizemol(newmol)
            if rmol is None:
                continue
            self.mutex.acquire() # r/w _step_count
            self._step_count += 1
            self.mutex.release()
            logstr = '  Step %5i   Comb %02i-%02i %42.4f ' \
                % (self._step_count, self.r6s[r6], molidx, rene)
            yield rmol, rene, logstr
            if self.maxsteps > 0 and self._step_count >= self.maxsteps:
                return

    def reorganizeresults(self):
        logging.debug('LoopClosure.enes: %s' % self.enes)
        logging.debug('LoopClosure.tasks: %s' % [(id(x[0]), x[1]) for x in self._tasks])
        self.tmp_mtxyz_file.seek(0)
        oldmols = mtxyz.Mtxyz(self.tmp_mtxyz_file)
        newidxs = [ene[1] for ene in self.enes 
                   if self.keeprange < 0.0
                      or ene[0] <= self.keepbound]
                        
        if self.config.getboolean('DEFAULT', 'out_mtxyz'):
            res = [None] * len(newidxs)
            for oldidx, oldmol in enumerate(oldmols.read_mol_as_string()):
                try:
                    newidx = newidxs.index(oldidx)
                    assert res[newidx] is None
                    res[newidx] = oldmol
                except ValueError:
                    pass
            for x in res:
                assert x is not None
            ofname = self.config.get('DEFAULT', 'out_mtxyz_fname')
            logging.debug('call self.backup')
            self.backup(ofname)
            logging.debug('return from self.backup')
            logging.info('write result to %s' % ofname)
            file(ofname, 'w').writelines(res)
        else:
            newmolnametmp = os.path.splitext(self.molfname)[0] \
                        + ".%0" + str(len(str(len(newidxs)))) + "i.xyz"
            for oldidx, oldmol in enumerate(oldmols.read_mol_as_string()):
                try:
                    newidx = newidxs.index(oldidx)
                except ValueError:
                    pass
                ofname = newmolnametmp % (newidx + 1)
                self.backup(ofname)
                file(ofname, 'w').write(oldmol)

        self.log('\nOldidx Newidx Ene(sort by Oldidx)\n')
        for oldidx in range(len(self.enes)):
            ene = self._tasks[oldidx][1]
            try:
                newidx = newidxs.index(oldidx)
            except ValueError:
                self.log('%6i %6s %.4f\n' % (oldidx+1, '', ene))
            else:
                self.log('%6i %6i %.4f\n' % (oldidx+1, newidx+1, ene))

        self.log('\nOldidx Newidx Ene(sort by Newidx)\n')
        for newidx, oldidx in enumerate(newidxs):
            self.log('%6i %6i %.4f\n' % (oldidx+1, newidx+1, self._tasks[oldidx][1]))
        self.log('\n')

    def log(self, msg, lvl=None):
        if lvl is None or lvl <= self.log_level:
            sys.stdout.write(msg)
            sys.stdout.flush()

    def is_valid(self, mol, ene):
        if ene < self.legal_min_ene:
            return 'L'
        if self.chiral_idxs \
                and tuple(chiral.chiral_types(mol, self.chiral_idxs)) \
                != self._chirals:
            return 'C'
        if self.check_minimal and not tinker.isminimal(mol, self.forcefield):
            return 'M'
        return 'V'
    
    # FIXME: we only need write mol once
    def _minimizemol(self, newmol):
        if self.check_energy_before_minimization:
            ene = tinker.analyze(newmol, self.forcefield)
            if ene >= self.minimal_invalid_energy_before_minimization:
                return None, None
        logging.debug('call tinker.newton_mol')
        logging.debug('  self.forcefield=%s' % self.forcefield)
        logging.debug('  self.minconverge=%s' % self.minconverge)
        logging.debug('  prefix=%s' % threading.currentThread().getName())
        res = self.min_func(newmol,
                            self.forcefield,
                            self.minconverge,
                            prefix=threading.currentThread().getName())
        logging.debug('return from tinker.newton_mol')
        return res
        
    
    # TODO: provide a fast algorithm if self.is_head_tail is false 
    # and self.is_achiral is false and self.loopstep is 0
    def _check_tor(self, mol1, mol2):
        tors1 = [mol1.calctor(x[0], x[1], x[2], x[3]) for x in self.cmptors]
        tors2 = [mol2.calctor(x[0], x[1], x[2], x[3]) for x in self.cmptors]
        diff = tordiff.torsdiff(tors1, tors2, 
                                self.is_achiral, 
                                self.head_tail, 
                                self.loopstep)
        res = diff < self.torerror_radian
#         if res:
#             logging.info('LoopClosure._check_tor: tors1: %s' % tors1)
#             logging.info('LoopClosure._check_tor: tors2: %s' % tors2)
#             logging.info('LoopClosure._check_tor: diff: %s < %s' % (diff, self.torerror_radian))
        return res

    def print_copyright(self):
        msg = 'CCS2 conformational search (itcc ' + itcc.__version__ + ')\n'
        host = "unknown host"
        try:
            host = str(socket.gethostbyaddr(socket.gethostname()))
        except:
            pass
        msg += 'running on %s\n' % host
        self.log(msg)

    def print_config(self):
        msg = '# config file begin\n'
        ofile = StringIO()
        self.config.write(ofile)
        msg += ofile.getvalue()
        ofile.close()
        msg += '# config file end\n'
        self.log(msg)
    
    def backup(self, fname):
        if not os.path.exists(fname): return
        i = 1
        while 1:
            new_fname = fname + '.~%i~' % i
            if not os.path.exists(new_fname):
                break
            i += 1
        logging.info("backup `%s' to `%s'" % (fname, new_fname))
        os.rename(fname, new_fname)

def getr6result(coords, r6, dismat, shakedata):
    r6 = list(r6)
    r6[0] = r6[0][-1:]
    r6[-1] = r6[-1][:1]
    type_ = r6type(r6)
    if type_ == (1, 1, 1, 1, 1, 1, 1):
        idxs = tuple(sum(r6, tuple()))
        return Mezei.R6(coords, idxs, dismat, shakedata)
    elif type_ == (1, 1, 2, 1, 2, 1, 1):
        idxs = tuple(sum(r6, tuple()))
        return Mezeipro.R6(coords, idxs, dismat, shakedata)
    elif type_ == (1, 2, 1, 2, 1, 2, 1):
        idxs = tuple(sum(r6, tuple()))
        return mezeipro2.R6(coords, idxs, dismat, shakedata)
    assert False, r6type(r6)

def r6type(r6):
    return tuple([len(x) for x in r6])

_moltypedict = {'peptide': peptide.Peptide}
def getmoltype(key):
    return _moltypedict.get(key, base.Base)

# TODO: if it's a chain
def getshakedata(mol, loop):
    result = {}
    dloop = loop * 2
    for idx, atomidx in enumerate(loop):
        refidxs = [atomidx, dloop[idx-1], dloop[idx+1]]
        sidechain_ = sidechain.getsidechain(mol, loop, atomidx)
        result[atomidx] = (refidxs, sidechain_)
    return result

def r6s2str(r6s):
    res = "This loop has %i R6 blocks:\n" % len(r6s)
    ofile = StringIO()
    pprint.pprint(r6s, ofile)
    res += ofile.getvalue()
    res += '\n'
    return res
