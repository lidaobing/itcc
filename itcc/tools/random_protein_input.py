import random

def random_protein_input(ifile, ofile):
    lines = ifile.readlines()
    assert len(lines) >= 5
    ofile.writelines(lines[:3])

    for i in range(3, len(lines)):
        line = lines[i]
        line = line.strip()
        if not line:
            break
        words = line.split(' ', 3)
        ofile.write("%s %s %s %s\n" % (words[0],
                                       random.uniform(-180, 180),
                                       random.uniform(-180, 180),
                                       words[3]))

    ofile.writelines(lines[i:])

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s <FILE|->\n'
                         % os.path.basename(sys.argv[0]))
        sys.exit(1)
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    else:
        ifile = sys.stdin
    random_protein_input(ifile, sys.stdout)

if __name__ == '__main__':
    main()
