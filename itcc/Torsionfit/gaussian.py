# $Id$
import os
from itcc.Molecule import atom, molecule

__revision__ = '$Rev$'

def hatree2kcalpermol(hatree):
    return 627.51 * float(hatree)

def kcalpermol2hatree(kcalpermol):
    return float(kcalpermol) / 627.51


def out2arch(ifname):

    TAILLINENUMBER = 100

    ifile = os.popen('tail -n %i %s' % (TAILLINENUMBER, ifname))

    state = False

    lines = ''

    for line in ifile:
        if not state:
            if line.startswith(' 1\\1\\'):
                state = True
                lines += line[1:-1]
                if lines.endswith('\\\\@'):
                    break
        else:
            lines += line[1:-1]
            if lines.endswith('\\\\@'):
                break

    ifile.close()

    lines = lines.split('\\')
    return lines

def out2ene(ifname):
    lines = out2arch(ifname)

    for x in lines:
        if x.startswith('HF='):
            x = x[3:]
            return [float(y) for y in x.split(',')]

    return None

def findstrline(outfname, keystr):
    result = []

    cmdline = 'grep -n -- "%s" %s' % (keystr, outfname)
    ifile = os.popen(cmdline)
    for line in ifile:
        result.append(int(line[:line.index(':')]))
    ifile.close()
    return result


def out2mol(outfname):
    result = []

    line1 = findstrline(outfname, "Optimized Parameters")
    line2 = findstrline(outfname, "Enter /home/user/g../l202\.exe")
    line3 = findstrline(outfname,
                        "---------------------------------------------------------------------")
    i2 = 0
    i3 = 0
    for i1, x in enumerate(line1):

        mol = molecule.Molecule()

        while line2[i2] < x:
            i2 += 1
        y = line2[i2-1]
        while line3[i3] < y:
            i3 += 1
        z1 = line3[i3+1]
        z2 = line3[i3+2]
        cmdline = 'head -n %i %s | tail -n %i' % \
                  (z2-1, outfname, z2-z1-1)
        ifile = os.popen(cmdline)

        for line in ifile:
            words = line.split()
            atm = atom.Atom(int(words[1]))
            atm.x = float(words[3])
            atm.y = float(words[4])
            atm.z = float(words[5])
            mol.atoms.append(atm)

        ifile.close()
        result.append(mol)
    return result
