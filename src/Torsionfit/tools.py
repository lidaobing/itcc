# coding: gb2312
# $Id$
# $Log: tools.py,v $
# Revision 1.6  2004/02/16 12:07:41  nichloas
# fix import Scientific.Statistics bug
#
# Revision 1.5  2004/02/04 06:21:30  nichloas
# *** empty log message ***
#
# Revision 1.4  2004/02/01 04:43:52  nichloas
# implement copy
#
# Revision 1.3  2003/11/20 16:45:03  nichloas
# add RMS, RMSD, etc.
#
# Revision 1.2  2003/11/20 12:06:16  nichloas
# use ctools version angle torsionangle
#
#


import math
import os
import types
import re
import select
import operator

from torsionfit.ctools import *

try:
    from Scientific.Statistics import *
    stdev = standardDeviation
except ImportError:

    def stdev(list):
        sum1 = float(sum(list))
        sum2 = float(sum(map(lambda x: x*x, list)))
        n = len(list)
        return math.sqrt((sum2 - sum1 * sum1 / n)/(n-1))

    standardDeviation = stdev
    
def split(s, seplist):
    s = [s]
    for x in seplist:
        res = []
        for y in s:
            res.extend(y.split(x))
        s = res
    return res

def vector(a, b):
    x = b[0] - a[0]
    y = b[1] - a[1]
    z = b[2] - a[2]
    return (x,y,z)

def crossmulti(a, b):
    x = a[1] * b[2] - a[2] * b[1]
    y = a[2] * b[0] - a[0] * b[2]
    z = a[0] * b[1] - a[1] * b[0]
    return (x, y, z)
def dotmulti(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def distance(a,b):
    dx = a[0] - b[0];
    dy = a[1] - b[1];
    dz = a[2] - b[2];

    return math.sqrt(dx*dx+dy*dy+dz*dz);

def distanceb(coords,a,b):
    return distance(coords[a], coords[b])


def findblanklines(lines):
    """
    search blank lines
    """

    return [i for i in range(len(lines)) if lines[i].strip() == '']

def listDirectory(directory, fileExtList):
    if type(fileExtList) == types.StringType:
        fileExtList = [fileExtList]
    fileExtList = [ext.upper() for ext in fileExtList]
    fileList = [os.path.join(directory, f) for f in os.listdir(directory) \
                if os.path.splitext(f)[1].upper() in fileExtList]
    return fileList

def changeExt(ifname, newext):
    (root, ext) = os.path.splitext(ifname)
    return root+newext

def RMSD(list1, list2):
    return RMS(map(operator.sub, list1, list2))

def RMS(list):
    sum2 = float(sum(map(lambda x: x*x, list)))
    n = len(list)
    return math.sqrt(sum2/n)

def STDD(list1, list2):
    return standardDeviation(map(operator.sub, list1, list2))





def MADM(l):
    """
    Mean of Abs of Diffrence of Median
    各数与中位数的差的绝对值平均值
    """
    m = median(l)
    return sum(map(lambda x, m=m: abs(x-m), l))/float(len(l))

def MADMD(list1, list2):
    return MADM(map(operator.sub, list1, list2))

## def average(list):
##     return float(sum(list))/len(list)

## def median(list):
##     "中位数"
##     list = list[:]
##     list.sort()
##     if len(list) % 2 == 1:
##         return list[len(list)/2]
##     else:
##         return (list[len(list)/2] + list[len(list)/2-1])/2.0
    

def datafreq(data, min, max, num):
    result = [0] * num
    step = float(max - min)/num

    for x in data:
        type = int((x - min)/step)
        if 0 <= type < num:
            result[type] += 1

    return result


from LinearAlgebra import solve_linear_equations
import Numeric

def linesearch(a, b):
    assert(len(a) == 3 and len(b) == 3)
    a = Numeric.array([[x*x, x, 1] for x in a])
    b = Numeric.array(b)

    x = solve_linear_equations(a,b)
    print x[0]
    print -0.5*x[1]/x[0]
    print x[2] - x[1]*x[1]/4/x[0]

def request(ifile, list, timeout = None):
    list = list[:]
    for i in range(len(list)):
        if not hasattr(list[i], 'search'):
            list[i] = re.compile(list[i])

    pool = ''

    while 1:
        data = ifile.readline()
        if data == '':
            raise EOFError
        pool += data
        for i in range(len(list)):
            m = list[i].search(pool)
            if m:
                return (i,m,pool)
        if timeout is not None:
            r,w,x = select.select([ifile], [], [], timeout)
            if not r:
                return None
    return None

if __name__ == '__main__':
    a = [-3.737, -3.403, -3.880]
    b = [2.330, 2.345, 2.348]
    x = linesearch(a,b)

    list = [2,3,4,2,1]
    
    print stdev([1,2,3])

    
    
    




        
            




