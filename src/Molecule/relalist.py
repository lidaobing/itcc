# $Id$
# $Log: relalist.py,v $
# Revision 1.4  2003/12/22 05:37:16  nichloas
# fix bug.
#
# Revision 1.3  2003/12/22 03:11:52  nichloas
# add imptors
#
# Revision 1.2  2003/12/01 07:59:19  nichloas
# bug fix.
#
# Revision 1.1.1.1  2003/11/20 06:12:42  nichloas
# Initial version
#
#


class Relalist:
    """
    Relalist: Relation list, include
    bonds
    angles
    torsions
    imptors

    Care:
    the index number of mol.connect is begin with 0
    and the bonds, angles, torsions's index is begin with 1
    """

    def __init__(self, mol = None):
        if mol is not None:
            mol.confirmconnect()
            self.bonds = genR(mol.connect)
            self.angles = genA(mol.connect)
            self.torsions = genD(mol.connect)
            self.imptors = genI(mol.connect)
        else:
            self.bonds = None
            self.angles = None
            self.torsions = None
            self.imptors = None

    def __eq__(self, other):
        return self.bonds == other.bonds and \
               self.angles == other.angles and \
               self.torsions == other.torsions and \
               self.imptors == other.imptors

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        result = []
        result.append('Bonds: %i\n' % len(self.bonds))
        for x in self.bonds:
            result.append(str(x)+'\n')

        result.append('\nAngles: %i\n' % len(self.angles))
        for x in self.angles:
            result.append(str(x)+'\n')

        result.append('\nTorsions: %i\n' % len(self.torsions))
        for x in self.torsions:
            result.append(str(x)+'\n')

        result.append('\nImptors: %i\n' % len(self.imptors))
        for x in self.imptors:
            result.append(str(x)+'\n')
        
        return ''.join(result)
        
        
def genR(conns, bias = 1):
    result = []
    for i in range(len(conns)):
        for x in conns[i]:
            if i < x:
                result.append((i+bias,x+bias))
    return result

def genA(conns):
    result = []
    for i in range(len(conns)):
        for j in range(len(conns[i])):
            for k in range(j+1,len(conns[i])):
                result.append((conns[i][j]+1, i+1, conns[i][k]+1))
    return result

def genD(conns):
    result = []
    Rs = genR(conns, 0)
    for x in Rs:
        if len(conns[x[0]]) == 1 or len(conns[x[1]]) == 1:
            continue
        for y in conns[x[0]]:
            if y == x[1]:
                continue
            for z in conns[x[1]]:
                if z == x[0] or z == y:
                    continue
                result.append((y+1, x[0]+1, x[1]+1, z+1))
    return result

def genI(conns):
    "generate improper torsions"
    result = []
    for i in range(len(conns)):
        if len(conns[i]) == 3:
            result.append((conns[i][0]+1, conns[i][1]+1, i+1, conns[i][2]+1))
    return result


