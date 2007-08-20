# $Id$

import sys

def get_record(ifile):
    rank = None
    for line in ifile:
        if line.startswith('USER    Cluster Rank ='):
            rank = int(line.split()[-1])
            break
        
    if rank is None:
        return None
    
    for line in ifile:
        if line.startswith('USER    RMSD from reference structure       ='):
            rmsd = float(line.split()[-2])
            break
    
    for line in ifile:
        if line.startswith('USER    Estimated Free Energy of Binding    ='):
            ene = float(line.split()[-3])
            break
    
    return (rank, rmsd, ene)


def dlg(ifile, ofile):
    res = {}
    while 1:
        record = get_record(ifile)
        if record is None:
            break
        if record[0] not in res:
            res[record[0]] = []
        res[record[0]].append(record[1:])
        
    ofile.write('rank\tcount\tmin(rmsd)\tmax(rmsd)\tmean(rmsd)\tmin(ene)\tmax(ene)\tmean(ene)\n')
    for k, v in sorted(res.items()):
        count = len(v)
        rmsds = [x[0] for x in v]
        enes = [x[1] for x in v]
        
        rmsd_min = min(rmsds)
        rmsd_max = max(rmsds)
        rmsd_mean = sum(rmsds)/count
        
        ene_min = min(enes)
        ene_max = max(enes)
        ene_mean = sum(enes)/count
        
        ofile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %
                    (k, count, rmsd_min, rmsd_max, rmsd_mean, ene_min, ene_max, ene_mean))

def main():
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s dlgfile\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    ifile = sys.stdin
    
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    
    dlg(ifile, sys.stdout)

if __name__ == '__main__':
    main()