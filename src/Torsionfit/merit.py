# $Id$

import operator
from itcc.Torsionfit import cmpmol
from itcc.Tinker import tinker
from itcc.Tools import tools

__revision__ = '$Rev$'

optimize = tinker.batchoptimize
energy = tinker.batchenergy

class Meritresult(dict):
    pass



def chkdeform(flist1, flist2):

    numdeformstru = 0
    data = cmpmol.batchcmpmolfile(flist1, flist2)

    for i in range(len(data)):
        x = data[i]
        ac = x.maxanglechange()
        tc = x.maxtorsionchange()
        print flist1[i], ac[0], ac[3], tc[0], tc[3]
        if x.maxanglechange() >= 5.0 or x.maxtorsionchange() >= 10.0:
            numdeformstru += 1

    return numdeformstru
            

def merit(param):
    applyprm(param)
    
    iflist, oflist, refene = getfilelist()
    optene = tinker.batchoptimize(iflist, oflist)
    difene = [x-y for x, y in zip(refene, optene)]
    result = tools.stdev(difene)

#    print chkdeform(iflist, oflist)

    return result

class Detailmerit(object):
    __slots__ = ['iflist',
                 'oflist',
                 'refene',
                 'optene',
                 'disres',
                 'result']
    def detailmerit(self, iflist, oflist, refene):
        self.iflist = iflist[:]
        self.oflist = oflist[:]
        self.refene = refene[:]
                
        result = {}

        optimize(iflist, oflist)
        optene = energy(oflist)
        difene = map(operator.sub, refene, optene)

        result['Energy RMS'] = tools.STDD(optene, refene)
        result['Energy UME'] = tools.MADMD(optene, refene)
        result['Energy MAX'] = (max(difene) - min(difene))/2.0

        disres = cmpmol.batchcmpmolfile(iflist, oflist)

        result['Displacement RMS'] = disres.disRMS()
        result['Displacement Mean'] = disres.dismean()
        result['Displacement MAX'] = disres.dismax()

        self.optene = optene
        self.disres = disres
        self.result = result

        return result
    
def applyprm(param, ifname = 'oplsaa-temp.prm', ofname = 'oplsaa-exp.prm'):
    ifile = file(ifname)
    ofile = file(ofname, 'w+')
    ofile.writelines(ifile.readlines())
    ifile.close()

    ofile.write(str(param))
    
    ofile.close()


def getfilelist(ifname = 'reference.csv'):
    ifile = file(ifname)
    lines = ifile.readlines()
    ifile.close()

    words = [x.split() for x in lines]

    iflist = [x[0] for x in words]
    oflist = [x[1] for x in words]
    reference = [float(x[2]) for x in words]

    return iflist, oflist, reference
    
def test2():
    iflist, refene = getfilelist()
    oflist = [x[:-4] + 'o' + x[-4:] for x in iflist]
    print chkdeform(iflist, oflist)
    




def test():
    from itcc.Tinker import parameter
    params = ((1,21,30,1,4.669,5.124,0.0),
              (1,1,30,21,-1.220,-0.126,0.422),
              (21,1,1,30,0.845,-0.962,0.713),
              (1,1,21,30,0.0,0.0,-0.553))


    objparams = parameter.Parameters()
    
    for x in params:
        objparams.append(parameter.Torsionparameter(*x))

    print merit(objparams)
        
if __name__ == '__main__':
    test()
    
    













