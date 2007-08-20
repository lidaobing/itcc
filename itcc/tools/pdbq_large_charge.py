# $Id$

import sys

def disq(coord1, coord2):
    return sum([(x1-x2)*(x1-x2) for x1,x2 in zip(coord1, coord2)])

def pdbq_large_charge(ifile, ofile, verbose):
    data = []
    for line in ifile:
        words = line.split()
        if words[0] == 'ATOM':
            idx = int(line[7:11])
            typ = line[12:16].strip()
            while '0' <= typ[0] <= '9':
                typ = typ[1:]
            coords = [float(line[x:x+8]) for x in range(30,54,8)]
            data.append((idx, typ, coords))
    
#    res = 0
#    for idx, typ, coords, charge in data:
#        if typ[0] in 'NPS':
#            totalcharges = []
#            for idx2, typ2, coords2, charge2 in data[:]:
#                if (typ2[0] == 'H' and disq(coords, coords2) < 1.69) \
#                    or (typ2[0] != 'H' and disq(coords, coords2) < 2.89):
#                    totalcharges.append(charge2)
#            if verbose:
#                ofile.write('%s\t%s\t%.3f\t%s\n' % (idx, typ[0], sum(totalcharges), ' '.join(['%.3f' % x for x in totalcharges])))
#            res += round(abs(sum(totalcharges)))
    
    typs = []
    neighs = [[] for i in range(len(data))]
    for i in range(len(data)):
        for j in range(i):
            if data[i][1][0] == 'H' or data[j][1][0] == 'H':
                if disq(data[i][2], data[j][2]) <= 1.69:
                    neighs[i].append(j)
                    neighs[j].append(i)
            else:
                if disq(data[i][2], data[j][2]) <= 2.89:
                    neighs[i].append(j)
                    neighs[j].append(i)
    
    for i in range(len(data)):
        typs.append(data[i][1][0] + str(len(neighs[i])))
    
    res = 0
    for i in range(len(data)):
        charge = 0
        if typs[i][0] == 'P':
            O1count = len([1 for x in neighs[i] if typs[x] in ('O1', 'o1')])
            if O1count == 4:
                charge = -3
            elif O1count == 3:
                charge = -2
            elif O1count == 2:
                charge = -1
        if typs[i][0] == 'C':
            O1count = len([1 for x in neighs[i] if typs[x] in ('O1', 'o1')])
            if O1count == 2:
                charge = -1
            if [typs[x] for x in neighs[i]] == ['N3'] * 3:
                charge = 1
        if typs[i][0] == 'S':
            O1count = len([1 for x in neighs[i] if typs[x] in ('O1', 'o1')])
            if O1count == 4:
                charge = -2
            elif O1count == 3:
                charge = -1
        
        if typs[i] == 'N4':
            charge = 1
        res += abs(charge)
        if verbose and charge != 0:
            ofile.write('%s\t%s\t%+i\n' % (data[i][0], typs[i][0], charge))
    ofile.write("%s\n" % res)

def main():
    args = sys.argv[1:]
    
    verbose = False
    if args and args[0] == '-v':
        verbose = True
        args = args[1:]
        
    if not args:
        import os.path
        sys.stderr.write('Usage: %s [-v] pdbqfname ...\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
        
    for fname in args:
        ifile = sys.stdin
        if fname != '-':
            ifile = file(fname)
            if verbose:
                sys.stdout.write("%s\n" % fname)
            pdbq_large_charge(ifile, sys.stdout, verbose)

if __name__ == '__main__':
    main()