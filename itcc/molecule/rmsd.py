# $Id$
# TODO: itcc-rmsd a b c should output:
# a b rmsd(a, b)
# a c rmsd(a, c)
# b c rmsd(b, c)

import sys
from itcc.molecule import _rmsd
from itcc.molecule import mtxyz
from itcc.core import frame

__revision__ = '$Rev$'
__all__ = ['rmsd']

debug = False

def rmsd_common(mol1, mol2, atoms1=None, atoms2=None):
    if debug:
        assert topeq(mol1, mol2)
    if atoms1 is None:
        coords1 = mol1.coords
    else:
        coords1 = mol1.coords.take(atoms1, axis=0)

    if atoms2 is None:
        coords2 = mol2.coords
    else:
        coords2 = mol2.coords.take(atoms2, axis=0)
    return (coords1, coords2)

def rmsd(mol1, mol2, atoms1=None, atoms2=None):
    coords1, coords2 = rmsd_common(mol1, mol2, atoms1, atoms2)
    return _rmsd.rmsd(coords1, coords2)

def rmsd2(mol1, mol2, atoms1=None, atoms2=None):
    coords1, coords2 = rmsd_common(mol1, mol2, atoms1, atoms2)
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
            "    %prog [options] mtxyzfname\n" \
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
    (options, args) = parser.parse_args()

    if len(args) not in (1, 2):
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

    from itcc.molecule import read
    ifiles = []
    for arg in args:
        if arg == '-':
            ifile = sys.stdin
        else:
            ifile = file(arg)
        ifiles.append(ifile)
    mol1 = read.readxyz(ifiles[0])
    if options.no_h:
        if atoms1 is None:
            atoms1 = range(len(mol1))
        atoms1 = [x for x in atoms1 if mol1.atoms[x].no != 1]

            
    for mol2 in mtxyz.Mtxyz(ifiles[-1]):
        if options.no_h:
            if atoms2 is None:
                atoms2_new = range(len(mol2))
            else:
                atoms2_new = atoms2
            atoms2_new = [x for x in atoms2_new if mol2.atoms[x].no != 1]
        else:
            atoms2_new = atoms2
        print rmsd_func(mol1, mol2, atoms1, atoms2_new)

def main_rmsd():
    main_common(rmsd)

def main_rmsd2():
    main_common(rmsd2)

if __name__ == '__main__':
    main_rmsd()
