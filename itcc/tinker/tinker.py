# -*- coding: utf-8 -*-
# $Id$

import os
import sys
import os.path
import tempfile
import itertools
import subprocess

from itcc.molecule import read, relalist, write

__revision__ = '$Rev$'

debug = False
curdir = False

TNK_ROOT = os.getenv("TNK_ROOT", '')    # use same environment with molden

if TNK_ROOT:
    TINKERDIR = os.path.join(TNK_ROOT, "bin/")
else:
    TINKERDIR = ""

_getparam_cache = {}
def getparam(key):
    if not _getparam_cache.has_key(key):
        _getparam_cache[key] = getparam_real(key)
    return _getparam_cache[key]

def getparam_real(key):    
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


def _writemoltotempfile(mol):
    ofile = tempfile.NamedTemporaryFile()
    write.writexyz(mol, ofile)
    ofile.flush()
    return ofile


def optimizemol(*args, **kwargs):
    return optimize_minimize_mol('optimize', *args, **kwargs)


def minimizemol(*args, **kwargs):
    return optimize_minimize_mol('minimize', *args, **kwargs)


def optimize_minimize_mol(cmdname, mol, forcefield, converge = 0.01, prefix=None):
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

    ifile = subprocess.Popen([progpath, ifname, forcefield, str(converge)],
                             stdout=subprocess.PIPE).stdout

    result = None

    lines = ifile.readlines()
    ifile.close()

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
    progpath = os.path.join(TINKERDIR, cmdname)
    command = '%s %s %s %f' % (progpath, ifname, forcefield, converge)
    if debug:
        print >> sys.stderr, command
    ifile = subprocess.Popen(command, shell=True,
                             stdout=subprocess.PIPE).stdout

    result = None

    lines = ifile.readlines()
    ifile.close()

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

    cmdname = 'vibrate'
    progpath = os.path.join(TINKERDIR, cmdname)
    if os.path.exists('/usr/bin/vibrate.tinker'):
        progpath = '/usr/bin/vibrate.tinker'
    forcefield = getparam(forcefield)

    command = '%s %s %s<<EOF\n\nEOF' % (progpath, molfname, forcefield)
    ifile = subprocess.Popen(command, shell=True,
                             stdout=subprocess.PIPE).stdout
    lines = ifile.readlines()

    for idx, line in enumerate(lines):
        if line.startswith(' Vibrational Frequencies (cm-1) :'):
            lines = lines[idx+2:]
            break

    counter = itertools.count(1)
    result = []
    for line in lines:
        if not line.strip(): break
        line = line[:-1]
        assert len(line) % 15 == 0, line
        # format (5(i5,f9.3,a1))
        for i in range(0, len(line), 15):
            assert int(line[i:i+5]) == counter.next(), line
            result.append(_vibratefloat(line[i+5:i+15]))

    ifile.close()
    molfile.close()

    return result


def isminimal(mol, forcefield):
    freqs = vibratemol(mol, forcefield)
    if freqs[0] >= 0:
        return True
    if freqs[6] <= 0:
        return False
    return abs(freqs[0]) < abs(freqs[6])
