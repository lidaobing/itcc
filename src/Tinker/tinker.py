# -*- coding: utf-8 -*-
# $Id$


import os
import sys
import os.path
import tempfile
import itertools
from itcc.Molecule import read, relalist, write

debug = False

TNK_ROOT = os.getenv("TNK_ROOT", "")    # use same environment with molden

if TNK_ROOT:
    TINKERDIR = os.path.join(TNK_ROOT, "bin/")
else:
    TINKERDIR = ""

PARAM = os.getenv("TNK_PRM_ROOT", "")
if not PARAM and TNK_ROOT:
    PARAM = os.path.join(TNK_ROOT, "params/")

minimize_count = 0


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
    if not forcefield.endswith(".prm"):
        forcefield = forcefield + ".prm"
    forcefield = os.path.join(PARAM, forcefield)

    ofile = tempfile.NamedTemporaryFile()
    ifname = ofile.name
    write.writexyz(mol, ofile)
    ofile.flush()

    ofname = ifname + '.xyz'

    command = '%s %s %s %f' % (progpath, ifname, forcefield, converge)
    ifile = os.popen(command)

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
        print >>sys.stderr, command
    ifile = os.popen(command)

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


def optimize(ifname, ofname = None, converge = 0.01):
    """optimize(ifname, ofname = None, converge = 0.01) -> Float
    optimized the mol specified by ifname, and return the optimized energy
    """

    progpath = os.path.join(TINKERDIR, "optimize")
    
    command = '%s %s %s %f' % (progpath, ifname, PARAM, converge)
    ifile = os.popen(command)

    result = None
    
    for line in ifile:
        if line.find('Function') != -1:
            result = float(line.split()[-1])
            break

    ifile.read() #让程序正常结束
    ifile.close()

    if ofname != None:
        os.rename(ifname + '_2', ofname)

    if result is None:
        raise RuntimeError, ifname
    
    return result

def energy(ifname):
    """energy(ifname) -> Float
    return the energy of the mol
    """
    command = '%sanalyze %s %s E' % (TINKERDIR, ifname, PARAM)
    ifile = os.popen(command)

    result = None

    for line in ifile:
        if line.find('Total Potential Energy :') != -1:
            result = float(line.split()[-2])
            break

    ifile.read() #让程序正常结束
    ifile.close()

    if result is None:
        raise RuntimeError, ifname

    return result
    

    
def optimizes(iflist, oflist = None, converge = 0.01):
    """optimizes(iflist, oflist = None, converge = 0.01) -> List of Float
    optimized the mols specified by iflist, and return the optimized energies
    """
    result = []
    if oflist == None:
        for ifname in iflist:
            result.append(optimize(ifname, None, converge))
    else:
        for ifname, ofname in zip(iflist, oflist):
            result.append(optimize(ifname, ofname, converge))
    return result

def energies(iflist):
    """energies(iflist) -> List of Float
    return the energy of the mols specified by iflist
    """
    result = []
    for ifname in iflist:
        result.append(energy(ifname))
    return result


def _vibratefloat(str):
    if str.endswith('I'):
        return -float(str[:-1])
    return float(str)

def vibratemol(mol, forcefield):
    molfile = _writemoltotempfile(mol)
    molfname = molfile.name

    cmdname = 'vibrate'
    progpath = os.path.join(TINKERDIR, cmdname)
    if not forcefield.endswith(".prm"):
        forcefield = forcefield + ".prm"
    forcefield = os.path.join(PARAM, forcefield)

    command = '%s %s %s<<EOF\n\nEOF' % (progpath, molfname, forcefield)
    ifile = os.popen(command)

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

        for i in range(0,len(words),2):
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
