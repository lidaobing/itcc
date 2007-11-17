import sys
import os.path

def ccslog2enestep(ifile, ofile):
    ok = False
    for line in ifile:
        if line.startswith('Oldidx Newidx Ene(sort by Newidx)'):
            ok = True
            break
    if not ok:
        return
    ene1 = ifile.next().split()[2]
    ene2 = ifile.next().split()[2]
    ofile.write('%s %s %s\n' % (ene1, ene2, float(ene2) - float(ene1)))

def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s <FILE>\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)

    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])

    ccslog2enestep(ifile, sys.stdout)

if __name__ == '__main__':
    main()
