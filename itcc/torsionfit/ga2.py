# $Id$
import random
import os
import math

__revision__ = '$Rev$'

cycle = 1
bestcycle = 0
best = []
bestmark = 1
limit = []

def stdev(list):
    n = len(list)
    sum = 0
    sum2 = 0
    for x in list:
        sum = sum + x
        sum2 = sum2 + x * x

    return math.sqrt((sum2 - sum * sum / n)/(n-1))

def init():
    global limit

    param = [0.254, -2.794,  2.652, 1.318, -4.287, -0.119, -1.803, -1.856]

    limit = [[x-1, x+1] for x in param]
    n = len(param)
    popu = n * 5

    list = []
    list.append(param)
    for i in range(1, popu):
        list.append([random.uniform(x[0], x[1]) for x in limit])

    return list

def wrtparam(param):
    ofile = file('tinker.key', 'w+')
    ofile.write(' parameters oplsaac\n')
    ofile.write(' torsion 30 1 1 21 %6.3f 0.0 1\n' % param[0])
    ofile.write(' torsion  1 1 1 21 %6.3f 0.0 1 %6.3f 180.0 2 %6.3f 0.0 3\n' % \
                (param[1], param[2], param[3]))
    ofile.write(' torsion 21 30 1 1 %6.3f 0.0 1 %6.3f 180.0 2 %6.3f 0.0 3\n' % \
                (param[4], param[5], param[6]))
    ofile.write(' torsion 1 1 21 30 %6.3f 0.0 3\n' % param[7])
    ofile.close()

def calene(fname):
    command = 'optimize %s 0.01' % fname
    out = os.popen(command)
    lines = out.readlines()
    out.close()

    command = 'rm -f %s_2' % fname
    os.system(command)

    for x in lines:
        if x.find('Final Function Value') != -1:
            x = x.split()
            result = float(x[-1])
            return result

def eval_(param):
    wrtparam(param)
    refdata = [0.952, 0.000, 0.901, 0.649, 1.013, 0.240, \
               0.007, 3.429, 1.838, 4.683, 4.161, 1.146, \
               2.360, 2.602, 1.070, 0.282, 0.534, 2.017]
    result = []
    for i in range(1,19):
        fname = '%02i.xyz' % i
        result.append(calene(fname))


    result = [result[i]-refdata[i] for i in range(len(result))]
    return stdev(result)

def mutation(list, limit, P = 0.1):
    for i in range(len(list)):
        for j in range(len(list[i])):
            if random.random() < P :
                list[i][j] = random.uniform(limit[j][0], limit[j][1])

def crossover(list, P = 0.5):

    n = len(list)
    length = len(list[0])
    l = range(n)
    random.shuffle(l)

    for i in range(0,n,2):
        a = l[i]
        b = l[i+1]
        point = random.randint(1,length-1)
        temp = list[a][:point] + list[b][point:]
        list[b] = list[b][:point] + list[a][point:]
        list[a] = temp




def findgood(list, mark):
    global bestmark
    global best
    global bestcycle

    if cycle == 1 or min(mark) < bestmark:
        bestmark = min(mark)
        best = list[mark.index(bestmark)][:]
        bestcycle = 0
        return True
    else :
        bestcycle = bestcycle + 1
        return False


def select(list, mark, P = 0.2):
    n = len(list)
    keep = int(n * (1-P))

    markb = mark[:]
    markb.sort()
    threshold = markb[keep]

    result = []
    for i in range(n):
        if mark[i] < threshold:
            result.append(list[i])

    list = result

def newrandom(list, limit):
    n = len(list[0]) * 5 - len(list)
    for i in range(n):
        list.append([random.uniform(x[0], x[1]) for x in limit])


if __name__ == '__main__':
    list = init()
    log = file('log', 'a+')

    for cycle in range(1,300):
        mark = []
        for x in list:
            mark.append(eval_(x))

        if findgood(list, mark):
            tmpstr = '[' + ', '.join(['%.3f' % x for x in best]) + ']'
            log.write('Cycle %i: %s %f\n' % (cycle, tmpstr, bestmark))
        else:
            log.write('Cycle %i: Finished\n' % cycle)
        log.flush()
        if bestcycle > 5:
            break

        select(list, mark)
        mutation(list, limit)
        crossover(list)
        newrandom(list, limit)

    log.close()
