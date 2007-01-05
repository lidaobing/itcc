# -*- coding: utf8 -*-
# $Id$

from itcc.molecule.relalist import Relalist

__revision__ = '$Rev$'

class Param:
    def __init__(self):
        self.typcls = {}
        self.param = {}

def bond_uni(l):
    "键编号正规化"
    r = list(l)
    assert len(r) == 2
    if r[0] > r[1]:
        r.reverse()
    return tuple(r)

def angle_uni(l):
    "键角编号正规化"
    r = list(l)
    assert len(r) == 3
    if r[0] > r[2]:
        r.reverse()
    return tuple(r)

def torsion_uni(l):
    "二面角标号正规化"
    r = list(l)
    assert len(r) == 4
    if r[1] > r[2] or (r[1] == r[2] and r[0] > r[3]):
        r.reverse()
    return tuple(r)

def imptor_uni(l):
    "imptor编号正规化"
    r = l[:2] + l[3:4]
    r.sort()
    r.insert(2, l[2])
    return r

def readprm(prmfile):
    ifile = file(prmfile)
    keys = ['forcefield',
            'vdwtype',
            'radiusrule',
            'radiustype',
            'radiussize',
            'epsilonrule',
            'torsionunit',
            'vdw-14-scale',
            'chg-14-scale',
            'dielectric',
            'atom',
            'vdw',
            'bond',
            'angle',
            'imptors',
            'torsion',
            'charge']

    result = Param()
    result.param['head'] = ''

    for line in ifile:
        words = line.split()
        if len(words) == 0 or words[0] not in keys:
            continue

        key = words[0]

        if key == 'atom':
            result.typcls[words[1]] = words[2]
            result.param['atom-' + words[1]] = line
        elif key in ['vdw', 'charge']:
            result.param[key + '-' + words[1]] = line
        elif key == 'bond':
            t = tuple(bond_uni([int(x) for x in words[1:3]]))
            result.param['bond-%i-%i' % t] = line
        elif key == 'angle':
            t = tuple(angle_uni([int(x) for x in words[1:4]]))
            result.param['angle-%i-%s-%i' % t] = line
        elif key == 'torsion':
            t = tuple(torsion_uni([int(x) for x in words[1:5]]))
            result.param['torsion-%i-%i-%i-%i' % t] = line
        elif key == 'imptors':
            t = tuple(imptor_uni([int(x) for x in words[1:5]]))
            result.param['imptor-%i-%i-%i-%i' % t] = line
        else:
            result.param['head'] += line
        
    ifile.close()
    return result

def molparam(mol, prmfile):
    param = readprm(prmfile)
    types = mol.gettypes()
    classes = [param.typcls[str(x)] for x in types]

    
    types_set = list(set(types))
    types_set.sort(lambda x, y: cmp(int(x), int(y)))
               
    classes_set = list(set(classes))
    classes_set.sort(lambda x, y: cmp(int(x), int(y)))
    
    head = param.param.get('head', '')

    print head

    for x in types_set:
        print param.param['atom-%s' % x],
    print 

    for x in types_set:
        print param.param['charge-%s' % x],
    print

    for x in classes_set:
        print param.param['vdw-%s' % x],
    print

    rl = Relalist(mol)

    bonds = set()
    for x in rl.bonds:
        bonds.add(tuple(bond_uni([int(classes[y-1]) for y in x])))
    bonds = list(bonds)
    bonds.sort()
    for x in bonds:
        print param.param['bond-%s-%s' % x],
    print
    
    angles = set()
    for x in rl.angles:
        angles.add(tuple(angle_uni([int(classes[y-1]) for y in x])))
    angles = list(angles)
    def angles_sort(x, y):
        if x[1] == y[1]:
            return cmp(x, y)
        else:
            return cmp(x[1], y[1])
    angles.sort(angles_sort)
    for x in angles:
        print param.param['angle-%s-%s-%s' % x],
    print

    torsions = set()
    for x in rl.torsions:
        cls = [int(classes[y-1]) for y in x]
        if cls[1] > cls[2] or (cls[1] == cls[2] and cls[0] > cls[3]):
            cls.reverse()
        torsions.add(tuple(cls))
        
    torsions = list(torsions)

    def torsions_sort(x, y):
        result = cmp(x[1:3], y[1:3])

        if result == 0:
            return cmp(x, y)
        else:
            return result

    torsions.sort(torsions_sort)
    for x in torsions:
        print param.param['torsion-%s-%s-%s-%s' % x],
    print

    imptors = set()
    for x in rl.imptors:
        imptors.add(tuple(imptor_uni([int(classes[y-1]) for y in x])))
    imptors = list(imptors)
    def imptor_sort(x, y):
        result = cmp(x[2], y[2])
        if result == 0:
            return cmp(x, y)
        else:
            return result
    imptors.sort(imptor_sort)
    for x in imptors:
        key = 'imptor-%s-%s-%s-%s' % x
        if param.param.has_key(key):
            print param.param[key],
    print
    

def main():
    import sys
    if len(sys.argv) != 3:
        print "Usage: %s xyzfile prmfile\n" % sys.argv[0]
        sys.exit(1)

    from itcc.Molecule import read
    mol = read.readxyz(sys.argv[1])

    molparam(mol, sys.argv[2])
    

if __name__ == '__main__':
    main()
