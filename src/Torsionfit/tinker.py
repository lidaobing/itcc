# -*- coding: utf-8 -*-
# $Id$


import os
import os.path
import read, relalist
import write

TNK_ROOT = os.getenv("TNK_ROOT", "")    # use same environment with molden



if TNK_ROOT:
    TINKERDIR = os.path.join(TNK_ROOT, "bin/")
else:
    TINKERDIR = ""

PARAM = os.getenv("TNK_PRM_ROOT", "")
if not PARAM and TNK_ROOT:
    PARAM = os.path.join(TNK_ROOT, "params/")

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

def optimizemol(mol, forcefield, converge = 0.01):
    """optimizemol(mol, forcefield, converge = 0.01) -> (Molecular, Float)
    optimized the mol, and return the optimized energy
    """
    progpath = os.path.join(TINKERDIR, "optimize")
    if not forcefield.endswith(".prm"):
        forcefield = forcefield + ".prm"
    forcefield = os.path.join(PARAM, forcefield)

    try:
        ifname = os.tmpnam()
    except RuntimeWarning:
        pass
    ofile = file(ifname, "w+")
    write.writexyz(mol, ofile)
    ofile.close()

    ofname = ifname + '.xyz'

    command = '%s %s %s %f' % (progpath, ifname, forcefield, converge)
    ifile = os.popen(command)

    result = None

    lines = ifile.readlines()
    ifile.close()
    os.remove(ifname)
    
    for line in lines:
        if line.find('Function') != -1:
            result = float(line.split()[-1])
            break


    if result is None:
        import sys
        sys.stdout.writelines(lines)
        raise RuntimeError, ifname

    newmol = read.readxyz(file(ofname))
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

batchoptimize = optimizes               # obsolete name

def energies(iflist):
    """energies(iflist) -> List of Float
    return the energy of the mols specified by iflist
    """
    result = []
    for ifname in iflist:
        result.append(energy(ifname))
    return result

batchenergy = energies                  # obsolete name


                     
        
