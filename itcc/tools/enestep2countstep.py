# $Id$

def enestep2countstep(ifile, enes, ofile, gm=None):
    data = []
    for line in ifile:
        words = line.split()
        assert len(words) == 2
        data.append((float(words[0]), int(words[1])))
    data.sort(cmp=lambda x,y: cmp(x[1], y[1]))

    ofile.write('#')
    for ene in enes:
        ofile.write(' %s' % ene)
    ofile.write('\n')

    count = [0] * len(enes)
    if gm is None:
        gm = min([x[0] for x in data])
    for ene, step in data:
        for idx, ene_ref in enumerate(enes):
            if 0 <= ene - gm <= ene_ref:
                count[idx] += 1
        ofile.write("%s %s\n" % (step, ' '.join([str(x) for x in count])))

def main():
    import sys
    import getopt
    opts, args = getopt.getopt(sys.argv[1:], 'b:', ['base='])
    base = None
    
    for o, a in opts:
        if o in ("-b", "--base"):
            base = float(a)
    
    if len(args) < 2:
        import os.path
        sys.stderr.write('usage: %s [-b BASE] <ifname|-> ene...\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)

    ifile = sys.stdin
    if args[0] != '-':
        ifile = file(args[0])
    enes = [float(x) for x in args[1:]]
    enestep2countstep(ifile, enes, sys.stdout, base)

if __name__ == '__main__':
    main()
