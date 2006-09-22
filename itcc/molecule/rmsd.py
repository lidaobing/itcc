# $Id$

import sys
from itcc.molecule import _rmsd
from itcc.molecule import mtxyz
from itcc.tools import frame

__revision__ = '$Rev$'
__all__ = ['rmsd']

debug = False

def rmsd(mol1, mol2, atoms1=None, atoms2=None):
    if debug:
        assert topeq(mol1, mol2)
    if atoms1 is None:
        coords1 = mol1.coords
    else:
        coords1 = [mol1.coords[i] for i in atoms1]

    if atoms2 is None:
        coords2 = mol2.coords
    else:
        coords2 = [mol2.coords[i] for i in atoms2]

    return _rmsd.rmsd(coords1, coords2)

def topeq(mol1, mol2):
    if len(mol1) != len(mol2):
        return False

    for i in range(len(mol1)):
        if mol1.atoms[i].no != mol2.atoms[i].no:
            return False
    return True

def usage(ofile):
    ofile.write('Usage:\n')
    ofile.write('    %s xyzfname1 mxyzfname2\n' % sys.argv[0])
    ofile.write('    %s mtxyzfname\n' % sys.argv[0])

def main():
    from optparse import OptionParser
    usage = "\n" \
            "    %prog [options] xyzfname1 xyzfname2\n" \
            "    %prog [options] mtxyzfname\n" \
            "    %prog -h"
    parser = OptionParser(usage=usage)
    parser.add_option("--atoms", dest="atoms",
                      help="only compare selected atoms, 1-based",
                      metavar="STRING")
    parser.add_option("--atomsfile", dest="atomsfile",
                      help="read the selected atoms from file",
                      metavar="FILE")
    parser.add_option("--atoms1", dest="atoms1",
                      help="the selected atoms for molecule 1",
                      metavar="STRING")
    parser.add_option("--atoms1file", dest="atoms1file",
                      help="read the selected atoms from file",
                      metavar="FILE")
    parser.add_option("--atoms2", dest="atoms2",
                      help="the selected atoms for molecule 2",
                      metavar="STRING")
    parser.add_option("--atoms2file", dest="atoms2file",
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
    mol1 = read.readxyz(file(args[0]))
    for mol2 in mtxyz.Mtxyz(file(sys.argv[-1])):
        print rmsd(mol1, mol2, atoms1, atoms2)

if __name__ == '__main__':
    main()
