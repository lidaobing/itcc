# -*- coding: utf-8 -*-
# $Id$

__revision__ = '$Rev$'

import os
import sys
import os.path
import tempfile
import itertools
import subprocess
import shutil

from itcc.molecule import read, relalist, write

debug = False
curdir = False

TNK_ROOT = os.getenv("TNK_ROOT", '')    # use same environment with molden

if TNK_ROOT:
    TINKERDIR = os.path.join(TNK_ROOT, "bin/")
else:
    TINKERDIR = ""

def _which(cmdname):
    if subprocess.call(['which', cmdname],
                       stdout=file('/dev/null', 'w')) == 0:
        return True
    else:
        return False

class Error(RuntimeError):
    def __init__(self, s):
        RuntimeError.__init__(self, 'cwd: %s\n%s' % (os.getcwd(), s))

class _Prepare:
    def __init__(self, curdir_):
        self.iscurdir = curdir_
        if not self.iscurdir:
            self.olddir = os.getcwd()
            self.newdir = tempfile.mkdtemp()
            os.chdir(self.newdir)

    def __del__(self):
        if self.iscurdir:
            return
        os.chdir(self.olddir)
        shutil.rmtree(self.newdir)

_GETPARAM_CACHE = {}
def getparam(key):
    if not _GETPARAM_CACHE.has_key(key):
        _GETPARAM_CACHE[key] = getparam_real(key)
    return _GETPARAM_CACHE[key]

def getparam_real(key):
    assert isinstance(key, str)
    if os.path.isfile(key):
        return os.path.abspath(key)
    if not key.endswith('.prm'):
        key += '.prm'
        if os.path.isfile(key):
            return os.path.abspath(key)
    assert not os.path.isabs(key)

    PRM_ROOT = os.getenv("TNK_PRM_ROOT", "")
    if PRM_ROOT:
        param = os.path.join(PRM_ROOT, key)
        if os.path.isfile(param):
            return os.path.abspath(param)

    if TNK_ROOT:
        param = os.path.join(TNK_ROOT, 'params', key)
        if os.path.isfile(param):
            return os.path.abspath(param)

    param = os.path.join('/usr/share/tinker/params', key)
    if os.path.isfile(param):
        return os.path.abspath(param)

    assert False


def constrain(ifname, param = None):
    """constrain(ifname, param = None) -> List of String
    return the content of the constrain key file based on mol specified by ifname.
    restrain all torsions on mol.
    """

    mol = read.readxyz(file(ifname))
    rel = relalist.Relalist(mol)
    lines = ['restrain-torsion %d %d %d %d\n' % x for x in rel.torsions]

    if param is not None:
        lines.append('parameters %s\n' % param)

    return lines


def _writemoltotempfile(mol, dir=None):
    if dir is None:
        dir = os.getcwd()
    ofile = tempfile.NamedTemporaryFile(dir=dir)
    write.writexyz(mol, ofile)
    ofile.flush()
    return ofile


def analyze(mol, forcefield):
    '''return the energy of mol'''

    prepare = _Prepare(curdir)
    
    molfile = _writemoltotempfile(mol)
    molfname = molfile.name

    cmdname = 'analyze'
    forcefield = getparam(forcefield)
    lines = subprocess.Popen([cmdname, molfname, forcefield, 'E'],
                             stdout=subprocess.PIPE).communicate()[0].splitlines()
    for line in lines:
        if 'Total' in line:
            try:
                return float(line.split()[4])
            except StandardError, e:
                if isinstance(e, (IndexError, ValueError)):
                    raise Error(''.join(lines))
                else:
                    raise
    raise Error(''.join(lines))

def optimize_mol(*args, **kwargs):
    return optimize_minimize_mol('optimize', *args, **kwargs)


def minimize_mol(*args, **kwargs):
    return optimize_minimize_mol('minimize', *args, **kwargs)


def optimize_minimize_mol(cmdname, mol, forcefield,
                          converge = 0.01, prefix=None):
    """optimizemol(mol, forcefield, converge = 0.01) -> (Molecule, Float)
    optimized the mol, and return the optimized energy
    """
    progpath = os.path.join(TINKERDIR, cmdname)
    forcefield = getparam(forcefield)

    if curdir:
        if prefix is None:
            ifname = 'tinker.xyz'
        else:
            ifname = prefix + '.xyz'
        ofile = file(ifname, 'w')
    else:
        ofile = tempfile.NamedTemporaryFile(suffix='.xyz')
        ifname = ofile.name
    write.writexyz(mol, ofile)
    ofile.flush()

    ofname = ifname + '_2'

    lines = subprocess.Popen([progpath, ifname, forcefield, str(converge)],
                             stdout=subprocess.PIPE).communicate()[0].splitlines()

    result = None

    for line in lines:
        if line.find('Function') != -1:
            result = float(line.split()[-1])
            break


    if result is None:
        sys.stdout.writelines(lines)
        raise RuntimeError, ifname
    try:
        newmol = read.readxyz(file(ofname))
    except:
        print ifname, ofname
        raise
    ofile.close()
    os.remove(ofname)
    if curdir:
        os.remove(ifname)

    return newmol, result


def minimize_file(ifname, forcefield, converge = 0.01):
    return optimize_minimize_file('minimize', ifname, forcefield, converge)


def optimize_file(ifname, forcefield, converge = 0.01):
    return optimize_minimize_file('optimize', ifname, forcefield, converge)


def optimize_minimize_file(cmdname, ifname, forcefield, converge = 0.01):
    ofname = ifname + '_2'
    lines = subprocess.Popen([cmdname, ifname, forcefield, str(converge)],
                             stdout=subprocess.PIPE).communicate()[0].splitlines()

    result = None

    for line in lines:
        if line.find('Function') != -1:
            result = float(line.split()[-1])
            break


    if result is None:
        sys.stdout.writelines(lines)
        raise RuntimeError, ifname
    try:
        newmol = read.readxyz(file(ofname))
    except:
        print ifname, ofname
        raise
    os.remove(ofname)

    return newmol, result

def newton_file(ifname, forcefield, converge = 0.01):
    ofname = ifname + '_2'
    lines = subprocess.Popen(['newton', ifname, forcefield, 'A', 'A', str(converge)],
                             stdout=subprocess.PIPE).communicate()[0].splitlines()

    result = None

    for line in lines:
        if line.find('Function') != -1:
            result = float(line.split()[-1])
            break

    if result is None:
        sys.stdout.writelines(lines)
        raise RuntimeError, ifname
    try:
        newmol = read.readxyz(file(ofname))
    except:
        print ifname, ofname
        raise
    os.remove(ofname)

    return newmol, result

def _vibratefloat(str_):
    assert len(str_) == 10, str_
    if str_[0] == '*':
        ret = 99999.999
    else:
        ret = float(str_[:-1])
    if str_.endswith('I'):
        return -ret
    return ret


def vibratemol(mol, forcefield):
    molfile = _writemoltotempfile(mol)
    molfname = molfile.name

    cmdnames = ('vibrate.tinker', 'vibrate')
    cmdname = None
    for x in cmdnames:
        if _which(x):
            cmdname = x
            break

    if cmdname is None:
        raise Error()
    
    forcefield = getparam(forcefield)

    lines = subprocess.Popen([cmdname, molfname, forcefield, '0'],
                             stdout=subprocess.PIPE).communicate()[0].splitlines()

    for idx, line in enumerate(lines):
        if line.startswith(' Vibrational Frequencies (cm-1) :'):
            lines = lines[idx+2:]
            break

    counter = itertools.count(1)
    result = []
    for line in lines:
        if not line.strip():
            break
        line = line[:-1]
        assert len(line) % 15 == 0, line
        # format (5(i5,f9.3,a1))
        for i in range(0, len(line), 15):
            assert int(line[i:i+5]) == counter.next(), line
            result.append(_vibratefloat(line[i+5:i+15]))

    molfile.close()

    return result


def isminimal(mol, forcefield):
    freqs = vibratemol(mol, forcefield)
    if freqs[0] >= 0:
        return True
    if freqs[6] <= 0:
        return False
    return abs(freqs[0]) < abs(freqs[6])

class NewtonMol(object):
    def __init__(self, log_iter=False):
        self.log_iter = log_iter
        self.iters = []

    def do_log_iter(self, lines):
        for idx, line in enumerate(lines):
            if line.startswith(' TNCG'):
                if idx > 2:
                    self.iters.append(int(lines[idx-2].split()[0]))
                return

    def newton_mol(self, mol, forcefield,
                   converge = 0.01, prefix=None):
        """newton_mol(mol, forcefield, converge = 0.01, prefix=None) -> (Molecule, Float)
        optimized the mol with newton, and return the optimized energy
        """
        forcefield = getparam(forcefield)

        if curdir:
            if prefix is None:
                ifname = 'tinker.xyz'
            else:
                ifname = prefix + '.xyz'
            ofile = file(ifname, 'w')
        else:
            ofile = tempfile.NamedTemporaryFile(suffix='.xyz')
            ifname = ofile.name
        write.writexyz(mol, ofile)
        ofile.flush()

        ofname = ifname + '_2'

        ifile = subprocess.Popen(['newton', ifname, forcefield, 'A', 'A', str(converge)],
                                 stdout=subprocess.PIPE).communicate()[0]

        result = None

        lines = ifile.splitlines()

        if self.log_iter:
            self.do_log_iter(lines)

        for line in lines:
            if line.startswith(' Final Function'):
                result = float(line.split()[-1])
                break


        if result is None:
            sys.stdout.writelines(lines)
            raise RuntimeError, ifname
        try:
            newmol = read.readxyz(file(ofname))
        except:
            print ifname, ofname
            raise
        ofile.close()
        os.remove(ofname)
        if curdir:
            os.remove(ifname)
        return newmol, result
    
    __call__ = newton_mol
    
newton_mol = NewtonMol()
