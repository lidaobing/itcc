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

TNK_ROOT = os.getenv("TNK_ROOT", '')    # use same environment with molden

if TNK_ROOT:
    TINKERDIR = os.path.join(TNK_ROOT, "bin/")
else:
    TINKERDIR = ""

minimize_count = 0

def getparam(key):
    if os.path.isfile(key):
        return key
    if not key.endswith('.prm'):
        key += '.prm'
        if os.path.isfile(key):
            return key
    assert not os.path.isabs(key)

    PRM_ROOT = os.getenv("TNK_PRM_ROOT", "")
    if PRM_ROOT:
        param = os.path.join(PRM_ROOT, key)
        if os.path.isfile(param):
            return param

    if TNK_ROOT:
        param = os.path.join(TNK_ROOT, 'params', key)
        if os.path.isfile(param):
            return param

    param = os.path.join('/usr/share/tinker/params', key)
    if os.path.isfile(param):
        return param

    assert False


def constrain(ifname, param = None):
    """constrain(ifname, param = None) -> List of String
    return the content of the constrain key file based on mol specified by ifname.
    restrain all torsions on mol.
    """

    mol = read.readxyz(ifname)
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


def optimizemol(mol, forcefield, converge = 0.01):
    return optimize_minimize_mol('optimize', mol, forcefield, converge)


def minimizemol(mol, forcefield, converge = 0.01):
    global minimize_count
    minimize_count += 1
    return optimize_minimize_mol('minimize', mol, forcefield, converge)


def optimize_minimize_mol(cmdname, mol, forcefield, converge = 0.01):
    """optimizemol(mol, forcefield, converge = 0.01) -> (Molecule, Float)
    optimized the mol, and return the optimized energy
    """
    progpath = os.path.join(TINKERDIR, cmdname)
    forcefield = getparam(forcefield)

    ofile = tempfile.NamedTemporaryFile()
    ifname = ofile.name
    write.writexyz(mol, ofile)
    ofile.flush()

    ofname = ifname + '.xyz'

    command = '%s %s %s %f' % (progpath, ifname, forcefield, converge)
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
    ofile.close()
    os.remove(ofname)

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
    if str_.endswith('I'):
        return -float(str_[:-1])
    return float(str_)


def vibratemol(mol, forcefield):
    molfile = _writemoltotempfile(mol)
    molfname = molfile.name

    cmdname = 'vibrate'
    progpath = os.path.join(TINKERDIR, cmdname)
    forcefield = getparam(forcefield)

    command = '%s %s %s<<EOF\n\nEOF' % (progpath, molfname, forcefield)
    ifile = subprocess.Popen(command, shell=True,
                             stdout=subprocess.PIPE).stdout

    result = []

    while True:
        if ifile.next().startswith(' Vibrational Frequencies (cm-1) :'):
            ifile.next()
            break

    counter = itertools.count(1)
    for line in ifile:
        words = line.split()
        if not words:
            break
        assert len(words) % 2 == 0

        for i in range(0, len(words), 2):
            assert int(words[i]) == counter.next()
            result.append(_vibratefloat(words[i+1]))

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
