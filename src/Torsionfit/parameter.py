# $Id$
# $Log: parameter.py,v $
# Revision 1.3  2004/06/03 08:47:44  nichloas
# * Torsionparameter fix bug
#
# Revision 1.2  2003/12/01 07:53:38  nichloas
# bug fix.
#
# Revision 1.1.1.1  2003/11/20 06:12:42  nichloas
# Initial version

#


class Parameter:
    pass

class Torsionparameter(Parameter):
    def __init__(self, *args):
        assert len(args) == 7, str(args)
        self.data = tuple(args)

    def __str__(self):
        return 'torsion   %4i %4i %4i %4i   %8.3f 0.0 1 %8.3f 180.0 2 %8.3f 0.0 3\n' % self.data
    


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


    
