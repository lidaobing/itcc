# $Id$
'''Deal with the tinker .prm file'''

from itcc.tinker import molparam

__revision__ = '$Rev$'
__all__ = ['Parameter', 'Torsionparameter', 'Parameters']

class Parameter:
    pass

class Torsionparameter(Parameter):
    def __init__(self, data):
        assert 7 <= len(data) <= 10, str(data)
        self.data = tuple(data)

    def __str__(self):
        result = 'torsion   %4i %4i %4i %4i  ' % tuple(self.data[:4])
        params = self.data[4:]
        for idx, param in enumerate(params):
            idx += 1
            if idx % 2 == 1:
                result += ' %8.3f 0.0 %i' % (param, idx)
            else:
                result += ' %8.3f 180.0 %i' % (param, idx)
        result += '\n'
        return result

class Parameters(list):
    def __init__(self, l = (), data = ()):
        assert len(l) == len(data), str(l) + '\n' + str(data)
        
        for i in range(len(l)):
            param = tuple(l[i]) + tuple(data[i])
            self.append(Torsionparameter(*param))

    def __str__(self):
        result = ''
        for x in self:
            result += str(x)

        return result

def readtorsionprm(prmfname, i, j, k, l):
    toridx = molparam.torsion_uni((i, j, k, l))
    ifile = file(prmfname)
    for line in ifile:
        words = line.split()
        if len(words) in [14, 17, 20, 23] \
               and words[0] == 'torsion' \
               and molparam.torsion_uni([int(x) for x in words[1:5]]) == toridx:
            fold = (len(words) - 5) // 3
            result = []
            for idx in range(fold):
                data = words[5+3*idx:8+3*idx]
                if idx % 2 == 0:
                    assert float(data[1]) == 0.0
                else:
                    assert float(data[1]) == 180.0
                assert int(data[2]) == idx + 1
                result.append(float(data[0]))
            ifile.close()
            return result
    return None
            
