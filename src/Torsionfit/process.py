# $Id$

import os

__revision__ = '$Rev$'

if __name__ == '__main__':

    os.system('grep -A 15 -B 4 Z-Matrix c3h6o2s3.out > log')

    ifile = file('log', 'r')
    lines = ifile.readlines()
    ifile.close()

    i = 0

    dict_ = {}

    while i < len(lines):
        fname = "%02i.xyz" % ((int(lines[i][56:60])+190)/10)
        coords = [x.split()[-3:] for x in lines[i+9:i+20]]
        dict_[fname] = coords
        i = i + 21

    symbols = ['C', 'H', 'H', 'H', 'C', 'O', 'O', 'C', 'H', 'H', 'H']

    str_ = ['  113     2     3     4     5',
           '  122     1',
           '  122     1',
           '  122     1',
           '  123     1     6     7',
           '  125     5     8',
           '  124     5',
           '  126     6     9    10    11',
           '  130     8',
           '  130     8',
           '  130     8']


    for fname, data in dict_.items():
        ofile = file(fname, 'w+')
        ofile.write('11\n')
        for i in range(len(data)):
            tmpstr = '%6d %2s  %12s%12s%12s %s\n' % \
                     (i+1, symbols[i], data[i][0], data[i][1], data[i][2], str_[i])
            ofile.write(tmpstr)
        ofile.close()

    
    
