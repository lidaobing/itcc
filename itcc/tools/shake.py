# $Id$

__revision__ = '$Rev$'

import sys
import random
import math
from itcc.molecule import read, molecule, write
from itcc.core import tools

first_offset = 10.0


class DatRecord:
    def __init__(self, line):
        words = line.split()
        assert len(words) in (3, 5)
        if len(words) == 5:
            self.type = 'BOND'
        else:
            self.type = 'VDW'
        self.idx1 = int(words[0]) - 1
        self.idx2 = int(words[1]) - 1
        self.idx1, self.idx2 \
          = min(self.idx1, self.idx2), max(self.idx1, self.idx2)
        if len(words) == 5:
            self.min = float(words[3])
            self.max = float(words[4])
            assert(self.min < self.max)
        else:
            self.min = float(words[2])
        assert(self.idx1 >= 0)
        assert(self.idx2 >= 0)

    def check(self, mol):
        if self.type == 'BOND':
            return self.min <= mol.calclen(self.idx1, self.idx2) <= self.max
        else:
            return self.min <= mol.calclen(self.idx1, self.idx2)

def read_dat(ifile):
    result = []
    for line in ifile:
        line = line.strip()
        if not line:
            continue
        if line[0] == '#':
            continue
        result.append(DatRecord(line))
    return result

def random_vec3(scale):
    return molecule.CoordType(random.uniform(-scale, scale),
                              random.uniform(-scale, scale),
                              random.uniform(-scale, scale))

def uniform_vec3(scale):
    z = random.uniform(-1, 1)
    r = math.sqrt(1 - z * z)
    angle = random.uniform(0, 2*math.pi)
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    return molecule.CoordType(x * scale, y * scale, z * scale)

def random_vec3_2(ref, min_dis, max_dis):
    return ref + uniform_vec3(random.uniform(min_dis, max_dis))

def new_struct(mol):
    result = mol.copy()
    for i in range(len(result)):
        result.coords[i] += random_vec3(first_offset)
    return result

def get_status(mol, dats):
    result2 = []
    for dat in dats:
        state = dat.check(mol)
        if not state:
            result2.append(dat)
    return result2


def shake3(r1, r2, new_dis):
    dr = r2 - r1
    dr = (new_dis / tools.length(dr) - 1.0) / 2.0 * dr
    return r1 - dr, r2 + dr

def shake2(mol, dats, err_dats):
    newmol = mol.copy()
#     idx = 0
    while True:
#         print idx
#         idx += 1
        finished = True
        for dat in err_dats:
            if not dat.check(newmol):
                finished = False
                if dat.type == 'BOND':
                    newmol.coords[dat.idx1], newmol.coords[dat.idx2] = \
                      shake3(newmol.coords[dat.idx1], newmol.coords[dat.idx2],
                             random.uniform(dat.min, dat.max))
                else:
                    newmol.coords[dat.idx1], newmol.coords[dat.idx2] = \
                      shake3(newmol.coords[dat.idx1], newmol.coords[dat.idx2],
                             random.uniform(dat.min, dat.min+2.0))
        if finished:
            break
    new_err_dats = get_status(newmol, dats)
    return newmol, new_err_dats

def shake1(mol, dats, ofile):
    for i in range(100):
        newmol = new_struct(mol)
        err_dats = get_status(newmol, dats)
        for j in range(500):
            if not err_dats:
                write.writexyz(newmol, ofile)
                return True
            print i, j, len(err_dats)
            random.shuffle(err_dats)
            newmol, err_dats = shake2(newmol, dats, err_dats)
    print 'failed.'
    return False

def shake(xyz_ifile, dat_ifile):
    mol = read.readxyz(xyz_ifile)
    dats = read_dat(dat_ifile)
    for i in range(1):
        ofile = file('ello%03i.xyz' % i, 'w')
        shake1(mol, dats, ofile)
        ofile.close()

def usage(ofile):
    import os.path
    ofile.write('Usage: %s xyzfile|- constrainfile|-\n'
                % os.path.basename(sys.argv[0]))
    ofile.write("don't use `-' twice\n")

def main():
    if len(sys.argv) != 3 \
       or (sys.argv[1] == '-' and sys.argv[2] == '-'):
        usage(sys.stderr)
        sys.exit(1)

    if sys.argv[1] == '-':
        xyz_ifile = sys.stdin
    else:
        xyz_ifile = file(sys.argv[1])

    if sys.argv[2] == '-':
        dat_ifile = sys.stdin
    else:
        dat_ifile = file(sys.argv[2])

    shake(xyz_ifile, dat_ifile)

if __name__ == '__main__':
    if not main():
        sys.exit(1)
