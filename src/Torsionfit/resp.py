# $Id$
"""
To: amber@cgl.ucsf.EDU
Subject: esp to resp 
Date: Wed, 21 Feb 96 13:09:38 -0800
From: "Jim Caldwell" <caldwell@heimdal.ucsf.EDU>

At long last:

To get electrostatic points from Gaussian94 in a form that
RESP understands follow the following simple recipe:

Add iop(6,33=2) to your gaussian command line viz.

# hf/sto-3g pop=mk iop(6/33=2)

or, for compatibility with the Cornell et al. 1995 force field,

# mp2/6-31g* pop=mk iop(6/33=2)

This is does NOT appear in the g94 manual, so trust me :-)

Run g94 

g94 < coords.in > out.file

Look in your g94 output for the number of atoms and esp points.
"""


import sys

__revision__ = '$Rev$'

def grepfile(ifname, keystr):
    ifile = file(ifname)
    lines = ifile.readlines()
    ifile.close()
    return [line for line in lines if keystr in line]

def readit(ifname, ofname):

    unit = 0.529177249
    
    lines1 = grepfile(ifname, 'Atomic Center ')
    lines2 = grepfile(ifname, 'ESP Fit')
    lines3 = grepfile(ifname, 'Fit   ')
    
    data1 = [x.split()[-3:] for x in lines1]
    data1 = [[float(x)/unit for x in y] for y in data1]
    
    data2 = [x.split()[-3:] for x in lines2]
    data2 = [[float(x)/unit for x in y] for y in data2]
    
    data3 = [float(x.split()[-1]) for x in lines3]

    assert(len(data2) == len(data3))

    ofile = file(ofname, 'w+')
    ofile.write('%5i%5i\n' % (len(data1), len(data2)))

    for x in data1:
        ofile.write(' '*16+'%16.6e%16.6e%16.6e\n' % (x[0], x[1], x[2]))
    for i in range(len(data2)):
        ofile.write('%16.6e%16.6e%16.6e%16.6e\n' %
                    (data3[i], data2[i][0], data2[i][1], data2[i][2]))
    ofile.close()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        readit(sys.argv[1], 'esp.dat')
    elif len(sys.argv) == 3:
        readit(sys.argv[1], sys.argv[2])
    else:
        print 'Usage: %s infile [outfile]' % sys.argv[0]
    
    
    
