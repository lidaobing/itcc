# $Id$

import sys
import getopt

def pdbqchargeshift(ifile, ofile, to):
    lines = ifile.readlines()
    chargesum = 0.0
    n = 0
    for line in lines:
        words = line.split()
        if words and words[0] in ('ATOM', 'HEATM'):
            chargesum += float(line[70:76])
            n += 1
    shift = 0.0
    if n != 0:
        shift = (chargesum - to) / n
    for idx, line in enumerate(lines):
        words = line.split()
        if words and words[0] in ('ATOM', 'HEATM'):
            lines[idx] = line[:70] \
                + '%6.3f' % (float(line[70:76]) - shift) \
                + line[76:]
    
    ofile.writelines(lines)

def usage(ofile):
    import os.path
    ofile.write('Usage: %s [-t charge] <pdbqfile|->\n'
                % os.path.basename(sys.argv[0]))

def main():
    to = 0.0
    
    opts, args = getopt.getopt(sys.argv[1:], 't:')
    
    for k, v in opts:
        if k == '-t':
            to = float(v)
   
    if len(args) != 1:
        usage(sys.stderr)
        sys.exit(1)
        
    ifile = sys.stdin
    if args[0] != '-':
        ifile = file(args[0])
    
    pdbqchargeshift(ifile, sys.stdout, to)

if __name__ == '__main__':
    main()