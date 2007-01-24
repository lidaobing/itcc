# $Id$

__all__ = ['chiral_type']

def elementwise(fn):
    def newfn(arg):
        if hasattr(arg,'__getitem__'):  # is a Sequence
            return type(arg)(map(fn, arg))
        else:
            return fn(arg)
    return newfn

@elementwise
def chiral_type(mol, idx):
    if mol.connect is None: return None
    connects = [i for i in range(len(mol)) if mol.connect[idx, i]]
    if len(connects) != 4: return None
    tor = mol.calctor(*connects)
    if tor > 0.0: return True
    if tor < 0.0: return False
    return None

chiral_types = chiral_type

def main():
    import sys
    if len(sys.argv) < 4:
        import os.path
        sys.stderr.write('Usage: %s --idx INDEX FILENAME...\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)

    idx = [int(x) - 1 for x in sys.argv[2].split()]

    from itcc.molecule import read
    for fname in sys.argv[3:]:
        sys.stdout.write("%s " % fname)
        mol = read.readxyz(file(fname))
        for x in idx:
            t = chiral_type(mol, x)
            if t is True:
                sys.stdout.write('A')
            elif t is False:
                sys.stdout.write('B')
            else:
                sys.stdout.write('C')
        sys.stdout.write('\n')
        sys.stdout.flush()

if __name__ == '__main__':
    main()
