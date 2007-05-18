import sys
from itcc.molecule import read
from itcc.tools import conffile

def read_corr(ifile):
    res = []
    for line in conffile(ifile):
        res.append([int(x)-1 for x in line.split()])
        assert len(res[-1]) == 2
    return res


def verify_correspoding(mol1, mol2, corr):
    d = [None] * len(corr)
    for x in corr:
        if d[x[0]] is not None:
            print 'duplicate %i in id1' % x[0]
            return False
        d[x[0]] = x[1]

    t = set()
    for x in corr:
        if x[1] in t:
            print 'duplicate %i in id2' % x[1]
            return False
        t.add(x[1])

    assert len(mol1) == len(mol2)
    assert len(mol1) == len(d)

    n = len(mol1)

    for i in range(n):
        for j in range(i):
          i2 = d[i]
          j2 = d[j]
          assert mol1.is_connect(i, j) == mol2.is_connect(i2, j2), (i,j,i2,j2)

    return True

def main():
    if len(sys.argv) != 4:
        import os.path
        sys.stderr.write('Usage: %s <mol1|-> <mol2|-> <corr|->\n'
                         % os.path.basename(sys.argv[0]))
        sys.exit(1)
    mol1_ifile = sys.stdin
    if sys.argv[1] != '-':
        mol1_ifile = file(sys.argv[1])
    mol1 = read.readxyz(mol1_ifile)

    mol2_ifile = sys.stdin
    if sys.argv[2] != '-':
        mol2_ifile = file(sys.argv[2])
    mol2 = read.readxyz(mol2_ifile)

    corr_ifile = sys.stdin
    if sys.argv[3] != '-':
        corr_ifile = file(sys.argv[3])
    corr = read_corr(corr_ifile)

    verify_correspoding(mol1, mol2, corr)

if __name__ == '__main__':
    main()
