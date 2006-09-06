# $Id$

'''output a param file that only include the param useful for one mol'''

import sys

from itcc.tinker import tinker, molparam
from itcc.molecule import read, tools, relalist

__revision__ = '$Rev$'

def subparam(molfname, param):
    ofile = sys.stdout
    param = tinker.getparam(param)
    moldata = getmoldata(molfname)
    lines = [line for line in file(param) if checkline(line, moldata)]
    lines = delblanklines(lines)
    ofile.writelines(lines)

def getmoldata(molfname):
    mol = read.readxyz(file(molfname))
    types = tools.gettypes(mol)

    result = {}
    result['atomtypes'] = set(types)
    subtypes = list(result['atomtypes'])
    typepairs = []
    for i, type_1 in enumerate(subtypes):
        for type_2 in subtypes[i:]:
            typepairs.append(molparam.bond_uni([type_1, type_2]))
    result['typepairs'] = set(typepairs)

    rela = relalist.Relalist(mol)
    result['bondtypes'] = set([molparam.bond_uni(gettype(bond, types))
                               for bond in rela.bonds])
    result['angletypes'] = set([molparam.angle_uni(gettype(angle, types))
                                for angle in rela.angles])
    result['torsiontypes'] = set([molparam.torsion_uni(gettype(torsion, types))
                                  for torsion in rela.torsions])

    return result

def gettype(atomidxs, types):
    return [types[idx] for idx in atomidxs]


def checkline(line, moldata):
    words = line.split()
    if not words:
        return True
    if words[0][0] == '#':
        return False
    key1 = words[0]
    if key1 in key2key:
        return key2key[key1](words, moldata)
    return True

def checkatomtypes(words, moldata):
    key = int(words[1])
    if key in moldata['atomtypes']:
        return True
    return False

def checktypepairs(words, moldata):
    key = molparam.bond_uni([int(words[1]), int(words[2])])
    if key in moldata['typepairs']:
        return True
    return False

def checkbondtypes(words, moldata):
    key = molparam.bond_uni([int(words[1]), int(words[2])])
    if key in moldata['bondtypes']:
        return True
    return False

def checkangletypes(words, moldata):
    key = molparam.angle_uni([int(words[1]), int(words[2]), int(words[3])])
    if key in moldata['angletypes']:
        return True
    return False

def checktorsiontypes(words, moldata):
    key = molparam.torsion_uni([int(words[1]), int(words[2]),
                                int(words[3]), int(words[4])])
    if key in moldata['torsiontypes']:
        return True
    return False

def delblanklines(lines):
    result = []
    isprevblankline = False
    for line in lines:
        if len(line.strip()) != 0:
            isprevblankline = False
            result.append(line)
        else:
            if isprevblankline:
                continue
            isprevblankline = True
            result.append(line)
    return result

def main():
    if len(sys.argv) != 3:
        import os.path
        print >> sys.stderr, 'Usage: %s mol param' % \
              os.path.basename(sys.argv[0])
        sys.exit(1)
    subparam(sys.argv[1], sys.argv[2])

key2key = {'atom': checkatomtypes,
           'vdw': checkatomtypes,
           'strbnd': checkatomtypes,
           'angang': checkatomtypes,
           'charge': checkatomtypes,
           'piatom': checkatomtypes,
           'vdwpr': checktypepairs,
           'hbond': checktypepairs,
           'bond': checkbondtypes,
           'bond3': checkbondtypes,
           'bond4': checkbondtypes,
           'bond5': checkbondtypes,
           'opbend': checkbondtypes,
           'strtors': checkbondtypes,
           'dipole': checkbondtypes,
           'dipole3': checkbondtypes,
           'dipole4': checkbondtypes,
           'dipole5': checkbondtypes,
           'pibond': checkbondtypes,
           'pibond4': checkbondtypes,
           'pibond5': checkbondtypes,
           'angle': checkangletypes,
           'angle3': checkangletypes,
           'angle4': checkangletypes,
           'angle5': checkangletypes,
           'electneg': checkangletypes,
           'torsion': checktorsiontypes,
           'torsion4': checktorsiontypes,
           'torsion5': checktorsiontypes,
           }


if __name__ == '__main__':
    main()
