# $Id$

import math

from itcc.molecule import mtxyz

def omega_type(mol, idxs):
    res = ''
    for idx in idxs:
        tor = mol.calctor(idx[0], idx[1], idx[2], idx[3])
        if -math.pi/2 <= tor < math.pi/2:
            res += 'C'
        else:
            res += 'T'
    return res

def main():
    import sys
    import getopt
    
    opts, args = getopt.getopt(sys.argv[1:], "vI:")
    
    verbose = False
    idx_file = None
    
    for k, v in opts:
        if k == '-v':
            verbose = True
        elif k == '-I':
            idx_file = v
    
    if idx_file is None or not args:
        import os.path
        sys.stderr.write('Usage: %s [-v] -I idxfile xyzfile...\n' 
                         % os.path.basename(sys.argv[0]))
        sys.exit(1)
        
    idxs = [[int(x)-1 for x in line.split()] for line in file(idx_file)]
    for idx in idxs:
        assert len(idx) == 4
        
    for fname in args:
        ifile = sys.stdin
        if fname != '-':
            ifile = file(fname)
        for mol in mtxyz.Mtxyz(ifile):
            if verbose:
                print fname,
            print omega_type(mol, idxs)
                        
if __name__ == '__main__':
    main()
