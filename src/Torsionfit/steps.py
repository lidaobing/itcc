# $Id$

import os, math
import Gnuplot

__revision__ = '$Rev$'

tangle = [[5,6,8,9],[5,6,8,10],[5,6,8,11]]
prm = ''
def vector(a, b):
    return [b[i] - a[i] for i in range(3) ]
def crossmulti(a, b):
    x = a[1] * b[2] - a[2] * b[1]
    y = a[2] * b[0] - a[0] * b[2]
    z = a[0] * b[1] - a[1] * b[0]
    return [x, y, z]
def dotmulti(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def _parsetemp(ifilename, ofilename, col):
    """
    parse one column of ifile to outfile.
    """
    
    ifile = file(ifilename, 'r')
    lines = ifile.readlines()
    ifile.close()

    lines = [line.split() for line in lines]
    lines = [x[col]+'\n' for x in lines]

    ofile = file(ofilename, 'w+')
    ofile.writelines(lines)
    ofile.close()

def _angle(a,b,c):
    """
    Caculation angle abc
    """

    rba = vector(b,a)
    rbc = vector(b,c)

    cosine = dotmulti(rba, rbc)/math.sqrt(dotmulti(rba, rba) * dotmulti(rbc,rbc))

    if cosine > 1: cosine = 1
    if cosine < -1: cosine = -1

    theta = math.acos(cosine)

    theta = theta*180.0/math.pi

    return theta

    
    

def _torsionangle(a,b,c,d):
    """
    Caculation torsion angle
    """


    rab = vector(a, b)
    rbc = vector(b, c)
    rcd = vector(c, d)

    rt = crossmulti(rab, rbc)
    ru = crossmulti(rbc, rcd)

    cosine = dotmulti(rt, ru) / math.sqrt(dotmulti(rt, rt) * dotmulti(ru, ru))

    if cosine > 1: cosine = 1
    if cosine < -1: cosine = -1
    
    phi = math.acos(cosine)
    
    if dotmulti(rab, ru) < 0:
        phi = -phi

    return phi


def _caltorsion(coord, list):
    return _torsionangle(coord[list[0]-1], coord[list[1]-1], coord[list[2]-1], coord[list[3]-1])


def step1():
    """
    First Step:
        Caculation energy of molecular in force field withour optimize.
    """
    tmpname = 'temp1'
    
    os.system('echo "E_mmbo dummy" > %s' % tmpname)
    for i in range(1,37):
        command = 'analyze %02i.xyz %s E | grep Total >> %s' % (i, prm, tmpname)
        os.system(command)

    _parsetemp(tmpname, 'step1.csv', -2)


def optimize():
    """
    Step 2:
        Optimize and caculation energy of molecular in force field.
    """

    tmpname = 'temp2'
    
    os.system('echo E_mm > %s' % tmpname)
    for i in range(1,19):
        command = 'optimize %02i %s 0.001 | grep Function >> %s' % (i, prm, tmpname)
        os.system(command)
        command = 'mv -f %02i.xyz_2 %02ia.xyz' % (i, i)
        os.system(command)

    _parsetemp(tmpname, 'step2.csv', -1)

def step3():
    """
    Step 3:
        Caculation energy of optimized molecular in force field without some torsion parameter.
    """

    tmpname = 'temp3'
    
    os.system('echo "E_mmwot dummy" > %s' % tmpname)
    for i in range(1,37):
        command = 'analyze %02ia.xyz oplsaah6 E | grep Total >> %s' % (i, tmpname)
        os.system(command)

    _parsetemp(tmpname, 'step3.csv', -2)

def step4():
    _step4('%02ia.xyz','step4.csv')

def step4_2():
    _step4('%02i.xyz', 'step4_2.csv')

def _step4(ifilename, ofilename):
    """
    Caculation MM Energy distribution.
    """

    tmpname = 'temp4'
    
    os.system('rm -f %s' % tmpname)
    for i in range(1,19):
        fname = ifilename % i
        command = 'analyze %s %s E | tail -n 6 >> %s' % (fname, prm, tmpname)
        os.system(command)

    ifile = file(tmpname, 'r')
    lines = ifile.readlines()
    ifile.close()

    lines = [line.split() for line in lines]

    ofile = file(ofilename, 'w+')

    ofile.write('\t'.join([' '.join(x[0:-2]) for x in lines[:5]]) + '\n')
    
    for i in range(0,108,6):
        ofile.write('\t'.join([lines[i+j][-2] for j in range(6)]) + '\n')

    ofile.close()

def step5():
    """
    Check the torsion angle after optimize
    """
    result = []
    for i in range(1, 37):
        ifile = file('%02ia.xyz' % i, 'r')
        lines = ifile.readlines()
        ifile.close()

        lines = lines[1:]
        lines = [x.split() for x in lines]
        lines = [x[2:5] for x in lines]
        lines = [[float(y) for y in x] for x in lines]

        tmpresult = [_caltorsion(lines,x) for x in tangle]
        result.append(tmpresult)

    ofile = file('step5.csv', 'w+')
    
    head = '\t'.join(['m' + '-'.join([str(y) for y in x]) for x in tangle]) + '\n'
    ofile.write(head)

    body = '\t'.join(['%10.5f'] * len(tangle)) + '\n'

    for x in result:
        ofile.write(body % tuple(x))
    ofile.close()


angle = [[5,6,8],[6,8,9],[6,8,10],[6,8,11]]
def _calangle(lines, x):
    return _angle(lines[x[0]-1], lines[x[1]-1], lines[x[2]-1])
    
def calangle():
    """
    Check the torsion angle after optimize
    """
    result = []
    for i in range(1, 37):
        ifile = file('%02i.xyz' % i, 'r')
        lines = ifile.readlines()
        ifile.close()

        lines = lines[1:]
        lines = [x.split() for x in lines]
        lines = [x[2:5] for x in lines]
        lines = [[float(y) for y in x] for x in lines]

        tmpresult = [_calangle(lines,x) for x in angle]
        result.append(tmpresult)

    ofile = file('anglebo.csv', 'w+')
    
    head = '\t'.join(['m' + '-'.join([str(y) for y in x]) for x in angle]) + '\n'
    ofile.write(head)

    body = '\t'.join(['%10.5f'] * len(angle)) + '\n'

    for x in result:
        ofile.write(body % tuple(x))
    ofile.close()

def step6():
    """
    Check the torsion angle before optimize
    """
    result = []
    for i in range(1, 37):
        ifile = file('%02i.xyz' % i, 'r')
        lines = ifile.readlines()
        ifile.close()

        lines = lines[1:]
        lines = [x.split() for x in lines]
        lines = [x[2:5] for x in lines]
        lines = [[float(y) for y in x] for x in lines]
        
        tmpresult = [_caltorsion(lines,x) for x in tangle]
        result.append(tmpresult)

    ofile = file('step6.csv', 'w+')
    
    head = '\t'.join(['q' + '-'.join([str(y) for y in x]) for x in tangle]) + '\n'
    ofile.write(head)

    body = '\t'.join(['%10.5f'] * len(tangle)) + '\n'

    for x in result:
        ofile.write(body % tuple(x))
    ofile.close()


def step7():
    """
    Combine all data in step 1 to step 6
    """
    lines = []
    for i in (0,1,2,4,6):
        ifile = file('step%i.dat' % i, 'r')
        lines.append(ifile.readlines())
        ifile.close()
        
    result = []

    for i in range(len(lines[0])):
        result.append('\t'.join([x[i][:-1] for x in lines]) + '\n')
    
    ofile = file('step7.dat', 'w+')
    ofile.writelines(result)

def step8():
    """
    print plot
    """

    ifile = file('step7.dat', 'r')
    lines = ifile.readlines()
    lines = [x.split('\t') for x in lines]
    title = lines[0]
    lines = lines[1:]


    da = title.index('q2-4-5-6')
    db = title.index('E_qm')
    dc = title.index('E_mmbo')
    dd = title.index('E_mm')
    de = title.index('E_mmwot')

    data1 = [[float(x[da]), float(x[db])] for x in lines]
    data2 = [[float(x[da]), float(x[dc])] for x in lines]
    data3 = [[float(x[da]), float(x[dd])] for x in lines]
    data4 = [[float(x[da]), float(x[de])] for x in lines]
    
    
    g = Gnuplot.Gnuplot()
    g.title('Torsion Energy')
    g('set data style linespoints')
    g.xlabel('Torsion angle of (2-4-5-6) (degree)')
    g.ylabel('Energy (kcal/mol)')
    g.plot(Gnuplot.Data(data1, title='E_{qm}'),
           Gnuplot.Data(data2, title='E_{mmbo}'),
           Gnuplot.Data(data3, title='E_{mm}'),
           Gnuplot.Data(data4, title='E_{mmwot}'))
    g.hardcopy('plot1.eps', enhanced=1, color=1)
    raw_input()

def step9():
    '''
    Generate octave input data
    '''

    ifile = file('step7.dat', 'r')
    lines = ifile.readlines()
    ifile.close()

    lines = [x.split('\t') for x in lines]
    title = lines[0]
    lines = lines[1:]

    da = title.index('q3-2-4-5')
    db = title.index('E_qm')
    dc = title.index('E_mmwot')
    
    data = [[str(float(x[da])), str(float(x[db])), str(float(x[dc]))] for x in lines]
    data = [' '.join(x) + '\n' for x in data]

    ofile = file('step9.dat', 'w+')
    ofile.write('#Created by python script\n')
    ofile.write('#name: data\n')
    ofile.write('#type: matrix\n')
    ofile.write('#rows: %i\n' % len(data))
    ofile.write('#columns: 3\n')
    ofile.writelines(data)

    ofile.close()
    
if __name__ == '__main__':
    optimize()
    #step1()
    #step2()
    #step3()
    #step4()
    #step4_2()
    #calangle()
    #step5()
    #step6()
    #step7()
    #step8()
    #step9()

    
    pass
    
