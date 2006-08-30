# $Id$

__all__ = ['parse_tinker_scan_log']

def parse_tinker_scan_log(ifile, ofile):
    results = []    
    for line in ifile:
        if 'Potential Surface Map' in line:
            results.append(line)

    results.sort(key=lambda x: float(x.split()[-1]))
    ofile.writelines(results) 

def _help(ofile):
    ofile.write('usage: parse_tinker_scan_log filename|-\n'
                'parse tinker scan log file\n')

def main():
    import sys

    if len(sys.argv) != 2:
        _help(sys.stderr)
        sys.exit(1)

    if sys.argv[1] == '-':
        ifile = sys.stdin
    else:
        ifile = file(sys.argv[1])

    parse_tinker_scan_log(ifile, sys.stdout)

if __name__ == '__main__':
    main()
