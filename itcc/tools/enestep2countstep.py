#!/usr/bin/env python

def enestep2countstep(ifile, enes, ofile):
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
    gm = min([x[0] for x in data])
    for ene, step in data:
        for idx, ene_ref in enumerate(enes):
            if ene - gm <= ene_ref:
                count[idx] += 1
        ofile.write("%s %s\n" % (step, ' '.join([str(x) for x in count])))

def main():
    import sys
    if len(sys.argv) < 3:
        import os.path
        sys.stderr.write('usage: %s ifname ene1 ene2 ...\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)

    ifile = file(sys.argv[1])
    enes = [float(x) for x in sys.argv[2:]]
    enestep2countstep(ifile, enes, sys.stdout)

if __name__ == '__main__':
    main()
