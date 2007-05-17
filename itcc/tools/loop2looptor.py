def loop2looptor(ifile, ofile):
    a = [int(x) for x in ifile.read().split()]
    a += a
    for i in range(len(a)/2):
        ofile.write('%i %i %i %i\n' % tuple(a[i:i+4]))

def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s loop\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    loop2looptor(file(sys.argv[1]), sys.stdout)

if __name__ == '__main__':
    main()
