import pkg_resources
import math

from itcc import tools

ff_cache = {}
caflisch_dat = None
r_probe = 1.4
pij_bonded = 0.8875
pij_nonbonded = 0.3516

class Caflisch(object):
    def __init__(self, data):
        self.data = data
        assert len(self.data) == 5

    def _r_min(self):
        return self.data[1]

    def _r(self):
        return self.data[2]

    def _p(self):
        return self.data[3]

    def _sigma(self):
        return self.data[4]

    r_min = property(_r_min)
    r = property(_r)
    p = property(_p)
    sigma = property(_sigma)

def init_caflisch():
    global caflisch_dat
    if caflisch_dat is not None: return
    caflisch_dat = read_caflisch(
        pkg_resources.resource_stream(__name__, 'caflisch.dat'))

def init_ff(forcefield):
    if forcefield in ff_cache:
        return
    init_caflisch()
    ff_cache[forcefield] = {}
    res = ff_cache[forcefield]

    ifname = forcefield + "-caflisch.dat"
    ifile = pkg_resources.resource_stream(__name__, ifname)

    for line in tools.conffile(ifile):
        ff_type, cal_type = (int(x) for x in line.split())
        if ff_type in res:
            raise RuntimeError("duplicate type")
        if cal_type != 0:
            res[ff_type] = caflisch_dat[cal_type]
        else:
            res[ff_type] = None

def solvent_caflisch(mol, forcefield, debug=0):
    if mol.connect is None:
        raise RuntimeError("can't deal with mol without connective information")
    
    init_ff(forcefield)
    ff = ff_cache[forcefield]
    
    data = []
    for i in range(len(mol)):
        if mol.atoms[i].type not in ff:
            raise RuntimeError(
                "no corresponding caflisch type for type %i of %s"
                % (mol.atoms[i].type, forcefield))
        if ff[mol.atoms[i].type] is not None:
            data.append((ff[mol.atoms[i].type], mol.coords[i], i))

    areas = []
    for i in range(len(data)):
        ri = data[i][0].r
        area = 1
        S = 4 * math.pi * (ri + r_probe) * (ri + r_probe)
        for j in range(len(data)):
            if j == i: continue
            rj = data[j][0].r

            rijsq = tools.dissq(data[i][1], data[j][1])
            max_r = data[i][0].r + data[j][0].r + r_probe * 2
            if rijsq >= max_r * max_r:
                continue

            rij = math.sqrt(rijsq)
            bij = math.pi * (ri + r_probe) * (max_r - rij) \
                * (1 + (rj - ri) / rij)

            bonded = mol.is_connect(data[i][2], data[j][2])
            if bonded:
                pij = pij_bonded
            else:
                pij = pij_nonbonded

            area *= 1 - data[i][0].p * pij * bij / S
        areas.append(area * S)

    if debug >= 1:
        for i in range(len(data)):
            print data[i][2]+1, areas[i]
    return sum(areas[i] * data[i][0].sigma for i in range(len(data)))

def read_caflisch(ifile):
    formats = (int, str, float, float, float, float)
    result = {}
    for line in ifile:
        line = line.strip()
        if not line: continue
        if line[0] == '#': continue
        words = line.split()
        assert len(words) == 6
        words = [format(x) for format,x in zip(formats, words)]
        assert words[0] not in result, "duplicates type in input file"
        result[words[0]] = Caflisch(tuple(words[1:]))
    return result

def main():
    import sys
    if len(sys.argv) != 3:
        import os.path
        sys.stderr.write('Usage: %s molname forcefield\n'
                         % os.path.basename(sys.argv[0]))
        sys.exit(1)
    from itcc.molecule import read
    mol = read.readxyz(file(sys.argv[1]))
    print solvent_caflisch(mol, sys.argv[2], 1)
    

if __name__ == '__main__':
    main()
