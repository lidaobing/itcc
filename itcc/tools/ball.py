# $Id$

import math
import random

def gen_coords(n):
    res = []
    for i in range(n):
        x = random.uniform(-2, 2)
        yz = math.sqrt(4 - x*x)
        phi = random.uniform(0, math.pi*2)
        y = yz * math.sin(phi)
        z = yz * math.cos(phi)
        res.append([x, y, z])
    return res
        
def coords2txyz(coords, ofile):
    ofile.write("%i\n" % (len(coords)+1))
    ofile.write("1 C 0.0 0.0 0.0 1\n")
    for i in range(len(coords)):
        c = coords[i]
        ofile.write("%i C %f %f %f 1\n" % (i+2, c[0], c[1], c[2]))
        
def gen_tinker_key(n, ofile):        
    ofile.write('RESTRAIN-POSITION 1\n')
    for i in range(n):
        ofile.write('RESTRAIN-DISTANCE %i %i 10000 1.0 1.0\n' % (1, i+2))
        
def gen_prm(ofile):        
    ofile.write('atom      1    C     "CSP3 ALKANE"             6     12.000     0\n'
                'vdw           1               0.5      0.044\n')

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s n\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    n = int(sys.argv[1])
    
    ofile1 = file('tmp.xyz', 'w')
    coords2txyz(gen_coords(n), ofile1)
    ofile1.close()
    
    ofile2 = file('tinker.key', 'w')
    gen_tinker_key(n, ofile2)
    ofile2.close()
    
    ofile3 = file('tmp.prm', 'w')
    gen_prm(ofile3)
    ofile3.close()
    
if __name__ == '__main__':
    main()
