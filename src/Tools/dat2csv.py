# $Id$
import sys

__revision__ = '$Rev$'

def dat2csv(ifname, ofname):
    ifile = file(ifname)
    lines = ifile.readlines()
    ifile.close()

    words = [x.split() for x in lines]

    ofile = file(ofname, 'w+')
    for x in words:
        for y in x:
            ofile.write(y + '\n')
    ofile.close()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        dat2csv(sys.argv[1], sys.argv[2])
    else:
        print 'Usage %s ifile ofile' % sys.argv[0]
