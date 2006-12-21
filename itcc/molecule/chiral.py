# $Id$

def chiral_type(mol, idx):
    if mol.connect is None: return None
    connects = [i for i in range(len(mol)) if mol.connect[idx, i]]
    if len(connects) != 4: return None
    tor = mol.calctor(*connects)
    if tor > 0.0: return True
    if tor < 0.0: return False
    return None

def main():
    import sys
    if len(sys.argv) < 3:
        import os.path
        sys.stderr.write('Usage: %s filename idx...\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)

    from itcc.molecule import read        
    mol = read.readxyz(file(sys.argv[1]))
    for x in sys.argv[2:]:
        t = chiral_type(mol, int(x) - 1)
        if t is True:
            sys.stdout.write('A')
        elif t is False:
            sys.stdout.write('B')
        else:
            sys.stdout.write('C')
    sys.stdout.write('\n')

if __name__ == '__main__':
    main()
