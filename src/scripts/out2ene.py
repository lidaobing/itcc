#!/usr/bin/env python
# $Id$

__revision__ = '$Rev$'

def out2ene(ifname):
    ifile = file(ifname)

    state = False
    
    lines = ''
    
    for line in ifile:
        if not state:
            if line.startswith(' 1\\1\\'):
                state = True
                lines += line[1:-1] 
                if lines.endswith('\\\\@'):
                    break
        else:
            lines += line[1:-1]
            if lines.endswith('\\\\@'):
                break

    ifile.close()

    lines = lines.split('\\')
    for x in lines:
        if x.startswith('HF='):
            x = x[3:]
            return [float(y) for y in x.split(',')]

    return None

def main():
    import sys
    if len(sys.argv) == 2:
        result = out2ene(sys.argv[1])
        if result:
            for x in result:
                print x
        else:
            print >> sys.stderr, "NO data found"
    else:
        print >> sys.stderr, "Usage: %s outfname" % sys.argv[0]

if __name__ == '__main__':
    main()
        

