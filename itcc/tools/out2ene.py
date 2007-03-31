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
            for y in x.split(','):
                yield float(y)

def main():
    import sys

    if len(sys.argv) >= 2:
        for fname in sys.argv[1:]:
            print fname, ' '.join(str(x) for x in out2ene(fname))
    else:
        print >> sys.stderr, "Usage: %s outfname..." % sys.argv[0]

if __name__ == '__main__':
    main()


