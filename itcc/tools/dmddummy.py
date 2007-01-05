# $Id$

__revision__ = '$Rev$'

from itcc.molecule import read, relalist

def dmddummy(xyzfname):
    mol = read.readxyz(file(xyzfname))
    rlist = relalist.Relalist(mol)
    tors = rlist.torsions

    for tor in tors:
        if mol.atoms[tor[0]].no == 1 or mol.atoms[tor[-1]].no == 1:
            print tor[0]+1, tor[-1]+1

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        print >> sys.stderr, "Usage: %s xyzfname" % os.path.basename(sys.argv[0])
        sys.exit(1)
    dmddummy(sys.argv[1])

if __name__ == '__main__':
    main()
