# $Id$

__revision__ = '$Rev$'

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
