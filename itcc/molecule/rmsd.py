# $Id$
# TODO: itcc-rmsd a b c should output:
# a b rmsd(a, b)
# a c rmsd(a, c)
# b c rmsd(b, c)

import sys
from itcc.molecule import read, _rmsd
from itcc.molecule import mtxyz
from itcc.core import frame

__revision__ = '$Rev$'
__all__ = ['rmsd']

debug = False

def cache_mol(fname1, mol_cache):
    if fname1 in mol_cache:
        mol1 = mol_cache[fname1]
    else:
        ifile1 = sys.stdin
        if fname1 != '-':
            ifile1 = file(fname1)
        mol1 = read.readxyz(ifile1)
        mol_cache[fname1] = mol1
    return mol1

def rmsd_common(mol1, mol2, atoms1=None, atoms2=None):
    if debug:
        assert topeq(mol1, mol2)
    if atoms1 is None:
        coords1 = mol1.coords
    else:
        coords1 = mol1.coords.take(tuple(atoms1), axis=0)

    if atoms2 is None:
        coords2 = mol2.coords
    else:
        coords2 = mol2.coords.take(tuple(atoms2), axis=0)
    return (coords1, coords2)

def rmsd(mol1, mol2, atoms1=None, atoms2=None, mirror=False, loop_step=None):
    coords1, coords2 = rmsd_common(mol1, mol2, atoms1, atoms2)
    coords2s = [coords2]
    if mirror:
        coords2s.append(-coords2)
    if loop_step is not None:
        for t in coords2s[:]:
            for i in range(loop_step, len(coords2), loop_step):
                idx = tuple(range(i, len(coords2)) + range(i))
                coords2s.append(t.take(idx, axis=0))
                
    return min([_rmsd.rmsd(coords1, x) for x in coords2s])

def rmsd2(mol1, mol2, atoms1=None, atoms2=None, mirror=False):
    coords1, coords2 = rmsd_common(mol1, mol2, atoms1, atoms2)
    if mirror:
        return min(_rmsd.rmsd2(coords1, coords2),
                   _rmsd.rmsd2(coords1, -coords2))
    else:
        return _rmsd.rmsd2(coords1, coords2)

def topeq(mol1, mol2):
    if len(mol1) != len(mol2):
        return False

    for i in range(len(mol1)):
        if mol1.atoms[i].no != mol2.atoms[i].no:
            return False
    return True

def main_common(rmsd_func):
    from optparse import OptionParser
    usage = "\n" \
            "    %prog [options] xyzfname1 xyzfname2\n" \
            "    %prog [options] -F FILE\n" \
            "    %prog -h"
    parser = OptionParser(usage=usage)
    parser.set_default("no_h", False)
    parser.add_option('-H', "--no-h", dest="no_h",
                      action="store_true",
                      help="does not include hydrogen")
    parser.add_option('-a', "--atoms", dest="atoms",
                      help="only compare selected atoms, 1-based",
                      metavar="STRING")
    parser.add_option('-A', "--atomsfile", dest="atomsfile",
                      help="read the selected atoms from file",
                      metavar="FILE")
    parser.add_option('-b', "--atoms1", dest="atoms1",
                      help="the selected atoms for molecule 1",
                      metavar="STRING")
    parser.add_option('-B', "--atoms1file", dest="atoms1file",
                      help="read the selected atoms from file",
                      metavar="FILE")
    parser.add_option('-c', "--atoms2", dest="atoms2",
                      help="the selected atoms for molecule 2",
                      metavar="STRING")
    parser.add_option('-C', "--atoms2file", dest="atoms2file",
                      help="read the selected atoms from file",
                      metavar="FILE")
    parser.add_option('-F', "--files", dest="files",
                      help="read the compare file lists from FILE",
                      metavar="FILE")
    parser.add_option('-s', '--loop-step', 
                      dest='loop_step',
                      type='int',
                      help='logical symmetry: loop step')
    parser.add_option('-m', '--mirror',
                      dest='mirror',
                      action='store_true',
                      help='also consider the mirror molecule')
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      help='be verbose')
    (options, args) = parser.parse_args()

    if len(args) == 2 and options.files is None:
        pass
    elif len(args) == 0 and options.files:
        pass
    else:
        parser.error("incorrect number of arguments")

    if (options.atoms and options.atomsfile) or \
       (options.atoms1 and options.atoms1file) or \
       (options.atoms2 and options.atoms2file):
        parser.error("options conflict")

    atoms1 = None
    atoms2 = None
    if options.atomsfile:
        options.atoms = file(options.atomsfile).read()
    if options.atoms:
        atoms1 = list(frame.parseframe(options.atoms))
        atoms2 = atoms1[:]
    if options.atoms1file:
        options.atoms1 = file(options.atoms1file).read()
    if options.atoms1:
        atoms1 = frame.parseframe(options.atoms1)

    if options.atoms2file:
        options.atoms2 = file(options.atoms2file).read()
    if options.atoms2:
        atoms2 = frame.parseframe(options.atoms2)

    filelists = []
    if options.files is not None:
        filelists = [line.split() for line in file(options.files).readlines()]
    else:
        filelists = [args]

    from itcc.molecule import read

    mol_cache = {}
    for filepair in filelists:
        fname1 = filepair[0]
        fname2 = filepair[1]
        if options.verbose:
            print fname1, fname2,
        mol1 = cache_mol(fname1, mol_cache)
        mol2 = cache_mol(fname2, mol_cache)

        if options.no_h:
            if atoms1 is None:
                atoms1 = range(len(mol1))
            atoms1 = [x for x in atoms1 if mol1.atoms[x].no != 1]

        if options.no_h:
            if atoms2 is None:
                atoms2_new = range(len(mol2))
            else:
                atoms2_new = atoms2
            atoms2_new = [x for x in atoms2_new if mol2.atoms[x].no != 1]
        else:
            atoms2_new = atoms2
        print rmsd_func(mol1, mol2, atoms1, atoms2_new, 
                        options.mirror, options.loop_step)

def main_rmsd():
    main_common(rmsd)

def main_rmsd2():
    main_common(rmsd2)

if __name__ == '__main__':
    main_rmsd()
