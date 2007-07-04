import sys
from itcc.molecule import read

def verifyloop(mol, loop):
    loop_set = set(loop)
    if len(loop_set) != len(loop):
        return False

    res = True
    for i in range(len(loop)):
        if not mol.is_connect(loop[i], loop[i-1]):
            print loop[i]+1, loop[i-1]+1
            res = False

    return res

def main():
    if len(sys.argv) != 3:
        import os.path
        sys.stderr.write('Usage: %s <mol|-> <loop|->\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    mol_ifile = sys.stdin
    if sys.argv[1] != '-':
        mol_ifile = file(sys.argv[1])
    mol = read.readxyz(mol_ifile)

    loop_ifile = sys.stdin
    if sys.argv[2] != '-':
        loop_ifile = file(sys.argv[2])
    loop = [int(x) - 1 for x in loop_ifile.read().split()]

    res = verifyloop(mol, loop)
    if res:
        print 'valid'
    else:
        print 'invalid'
        sys.exit(1)

if __name__ == '__main__':
    main()
