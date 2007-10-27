# $Id$

import sys
from itcc.molecule import read, write

__revision__ = '$Rev$'

def _gettypes(typefile):
    for line in typefile:
        for word in line.split():
            yield int(word)

def settype(xyzfile, typefile):
    mol = read.readxyz(xyzfile)
    types = tuple(_gettypes(typefile))
    assert len(mol) == len(types), "%s - %s" % (len(mol), len(types))
    for idx, atype in enumerate(types):
        mol.settype(idx, atype)
    write.writexyz(mol, sys.stdout)
    
def settype2(xyzfile, types, ofile):
    line = xyzfile.readline()
    assert int(line.split()[0]) == len(types)
    
    ofile.write(line)
    for t in types:
        words = xyzfile.readline().split()
        words[5] = t
        ofile.write(' '.join(words) + '\n')
    
def main():
    if len(sys.argv) < 3:
        import os.path
        print >> sys.stderr, "Usage: %s {TYPEFNAME|-} {XYZFNAME|-}..." % \
              os.path.basename(sys.argv[0])
        sys.exit(1)

    if sys.argv[1] == '-':
        typefile = sys.stdin
    else:
        typefile = file(sys.argv[1])
        
    types = typefile.read().split()
    for fname in sys.argv[2:]:
        ifile = sys.stdin
        if fname != '-':
            ifile = file(fname)
        settype2(ifile, types, file(ifile.name+'_2', 'w'))

if __name__ == '__main__':
    main()
