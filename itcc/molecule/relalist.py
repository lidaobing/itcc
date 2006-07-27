# $Id$

__all__ = ['Relalist', 'genconns', 'genR', 'genA', 'genD', 'genI']
__revision__ = '$Rev$'

class Relalist:
    """
    Relalist: Relation list, include
    bonds
    angles
    torsions
    imptors
    """

    def __init__(self, mol = None):
        if mol is not None:
            mol.confirmconnect()
            conns = genconns(mol.connect)
            self.bonds = genR(conns)
            self.angles = genA(conns)
            self.torsions = genD(conns)
            self.imptors = genI(conns)
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
        convfun = lambda seq: str(tuple([x+1 for x in seq])) + '\n'
        result = []
        result.append('Bonds: %i\n' % len(self.bonds))
        result.extend([convfun(x) for x in self.bonds])

        result.append('\nAngles: %i\n' % len(self.angles))
        result.extend([convfun(x) for x in self.angles])

        result.append('\nTorsions: %i\n' % len(self.torsions))
        result.extend([convfun(x) for x in self.torsions])

        result.append('\nImptors: %i\n' % len(self.imptors))
        result.extend([convfun(x) for x in self.imptors])
        
        return ''.join(result)
        
        
def genconns(connect):
    result = []
    size = len(connect)
    for i in range(size):
        result.append([])
        for j in range(size):
            if connect[i][j]:
                result[-1].append(j)
    return result

def genR(conns):
    result = []
    for i in range(len(conns)):
        for x in conns[i]:
            if i < x:
                result.append((i, x))
    return result

def genA(conns):
    result = []
    for i in range(len(conns)):
        for j in range(len(conns[i])):
            for k in range(j+1, len(conns[i])):
                result.append((conns[i][j], i, conns[i][k]))
    return result

def genD(conns):
    result = []
    Rs = genR(conns)
    for x in Rs:
        if len(conns[x[0]]) == 1 or len(conns[x[1]]) == 1:
            continue
        for y in conns[x[0]]:
            if y == x[1]:
                continue
            for z in conns[x[1]]:
                if z == x[0] or z == y:
                    continue
                result.append((y, x[0], x[1], z))
    return result

def genI(conns):
    "generate improper torsions"
    result = []
    for i in range(len(conns)):
        if len(conns[i]) == 3:
            result.append((conns[i][0]+1, conns[i][1]+1, i+1, conns[i][2]+1))
    return result


