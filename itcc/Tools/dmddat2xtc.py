# $Id$

__revision__ = '$Rev$'

from itcc.Tools import _gmx_xtcio
from itcc.Tools import dmddat

def dmddat2xtc(ifile, ofname):
    aDmddat = dmddat.Dmddat(ifile)
    xtc = _gmx_xtcio.open_xtc(ofname, "w");
    box = ((aDmddat.boxsize[0]/10.0, 0.0, 0.0),
           (0.0, aDmddat.boxsize[1]/10.0, 0.0),
           (0.0, 0.0, aDmddat.boxsize[2]/10.0))
    for idx, frame in enumerate(aDmddat):
        time = frame.time
        frame = frame.coords
        frame = tuple([tuple([y/10.0 for y in x]) for x in frame])
        _gmx_xtcio.write_xtc(xtc, aDmddat.beadnum, idx+1, time,
                             box, frame, 1000.0)
    _gmx_xtcio.close_xtc(xtc);

def main():
    import sys
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: %s {dmddatfname|-} xtcfname\n" % sys.argv[0]);
        sys.exit(1)

    if sys.argv[1] == '-':
        dmddat_ifile = sys.stdin
    else:
        dmddat_ifile = file(sys.argv[1], 'rb')

    dmddat2xtc(dmddat_ifile, sys.argv[2])

if __name__ == '__main__':
    main()
