# $Id$

import sys

class Result(object):
    pass

def disq(coord1, coord2):
    return sum([(x1-x2)*(x1-x2) for x1,x2 in zip(coord1, coord2)])

def pdbq_large_charge(ifile, ofile=sys.stdout, verbose=0):
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
    
    res = []
    for i in range(len(data)):
        charge = 0
        actives = []
        if typs[i][0] == 'P':
            typ = 'P'
            actives.extend([x for x in neighs[i] if typs[x] in ('O1', 'o1')])
            O1count = len([1 for x in neighs[i] if typs[x] in ('O1', 'o1')])
            if O1count == 4:
                charge = -3
            elif O1count == 3:
                charge = -2
            elif O1count == 2:
                charge = -1
        if typs[i][0] == 'C':
            O1count = len([1 for x in neighs[i] if typs[x] in ('O1', 'o1')])
            S1count = len([1 for x in neighs[i] if typs[x] == 'S1'])
            N3count = len([1 for x in neighs[i] if typs[x] == 'N3'])
            if O1count == 2:
                actives = [x for x in neighs[i] if typs[x] in ('O1', 'o1')]
                typ = 'CO'
                charge = -1
            if [typs[x] for x in neighs[i]] == ['N3'] * 3:
                typ = 'CN'
                charge = 1
            if typs[i] == 'C3' and N3count == 2 and O1count == 0 and S1count == 0:
                typ = 'CN'
                charge = 1
            if charge != 0 and typ == 'CN':
                Ns = [x for x in neighs[i] if typs[x] == 'N3']
                for x in Ns:
                    actives.extend([y for y in neighs[x] if typs[y] == 'H1'])
                
        if typs[i][0] == 'S':
            typ = 'S'
            O1count = len([1 for x in neighs[i] if typs[x] in ('O1', 'o1')])
            actives.extend([x for x in neighs[i] if typs[x] in ('O1', 'o1')])
            if O1count == 4:
                charge = -2
            elif O1count == 3:
                charge = -1
        
        if typs[i] == 'N4':
            typ = 'N'
            charge = 1
            actives.extend([y for y in neighs[i] if typs[y] == 'H1'])
            
        if charge != 0:
            t = Result()
            t.idx = i
            t.charge = charge
            t.type = typ
            t.actives = actives
            res.append(t)
        if verbose >= 2 and charge != 0:
            ofile.write('%s\t%s\t%+i\t%s\n' % (data[i][0], typs[i][0], charge, ' '.join([str(x+1) for x in actives])))
    if verbose >= 1:
        ofile.write("%s\n" % sum([abs(x.charge) for x in res]))
    return res

def main():
    args = sys.argv[1:]
    
    verbose = 1
    if args and args[0] == '-v':
        verbose = 2
        args = args[1:]
        
    if not args:
        import os.path
        sys.stderr.write('Usage: %s [-v] pdbqfname ...\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
        
    for fname in args:
        ifile = sys.stdin
        if fname != '-':
            ifile = file(fname)
            if verbose >= 2:
                sys.stdout.write("%s\n" % fname)
            pdbq_large_charge(ifile, sys.stdout, verbose)

if __name__ == '__main__':
    main()