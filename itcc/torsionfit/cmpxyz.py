# $Id$
import math
from itcc.Molecule import read, relalist
from itcc.Tools import tools

__revision__ = "$Rev$"

def maxb(seq):
    m = 0
    for i in range(1, len(seq)):
        if seq[i] > seq[m]:
            m = i
    return m
            
    

def cmpxyz(ifname1, ifname2):
    conns = read.readconns(ifname1)

    Rs = relalist.genR(conns)
    As = relalist.genA(conns)
    Ds = relalist.genD(conns)
    
    xyz1 = read.readxyz_2(ifname1)
    xyz2 = read.readxyz_2(ifname2)

    Rds1 = [tools.distance(xyz1[x[0]], xyz1[x[1]]) for x in Rs]
    Rds2 = [tools.distance(xyz2[x[0]], xyz2[x[1]]) for x in Rs]
    
    Ads1 = [tools.angle(xyz1[x[0]], xyz1[x[1]], xyz1[x[2]]) for x in As]
    Ads2 = [tools.angle(xyz2[x[0]], xyz2[x[1]], xyz2[x[2]]) for x in As]

    Dds1 = [tools.torsionangle(xyz1[x[0]], xyz1[x[1]], xyz1[x[2]], xyz1[x[3]]) \
            for x in Ds]
    Dds2 = [tools.torsionangle(xyz2[x[0]], xyz2[x[1]], xyz2[x[2]], xyz2[x[3]]) \
            for x in Ds]

    dR = [math.fabs(Rds1[i] - Rds2[i]) for i in range(len(Rds1))]
    dA = [math.fabs(Ads1[i] - Ads2[i]) for i in range(len(Ads1))]
    dD = [math.fabs(Dds1[i] - Dds2[i]) for i in range(len(Dds1))]

    M = maxb(dR)
    print 'max R diff: %f, R(%i, %i)' % (dR[M], Rs[M][0]+1, Rs[M][1]+1)

    M = maxb(dA)
    print 'max angle diff: %f, A(%i, %i, %i)' % \
          (dA[M], As[M][0]+1, As[M][1]+1, As[M][2]+1)

    M = maxb(dD)
    print 'max torsion diff: %f, D(%i, %i, %i, %i)' % \
          (dD[M], Ds[M][0]+1, Ds[M][1]+1, Ds[M][2]+1, Ds[M][3]+1)

    
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        cmpxyz(sys.argv[1], sys.argv[2])
        

         
    

    
    
