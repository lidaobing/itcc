#! /usr/bin/env python

import tools
import os

def xyz2pdb(ifname, ofname):
    ifile = file(ifname)
    lines = ifile.readlines()
    ifile.close()

    lines = lines[1:]
    words = [x.split() for x in lines]

    ofile = file(ofname, 'w+')
    for x in words:
        no = int(x[0])
        symbol = x[1]
        cx = float(x[2])
        cy = float(x[3])
        cz = float(x[4])
        ofile.write('HETATM %4i  %s %11i      %6.3f  %6.3f  %6.3f\n' % \
                    (no, symbol, no, cx, cy, cz))
    for x in words:
        conn = ['%5i' % int(y) for y in x[6:]]
        conn = ''.join(conn)
        ofile.write('CONECT %4i%s\n' % \
                    (int(x[0]), conn))
    ofile.write('END\n')
    ofile.close()

def xyz2pdb_all():
    ifilelist = tools.listDirectory(os.getcwd(), ['.xyz'])
    ofilelist = [tools.changeExt(x, '.ent') for x in ifilelist]
    for ifile, ofile in zip(ifilelist, ofilelist):
        xyz2pdb(ifile, ofile)
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        xyz2pdb(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] == 'all':
        xyz2pdb_all()
    else :
        print 'Usage: %s ifile ofile' % sys.argv[0]
        print 'or     %s all' % sys.argv[0]
        
        
