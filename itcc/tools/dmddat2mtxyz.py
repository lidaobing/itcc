# $Id$

__revision__ = '$Rev$'

from itcc.tools import dmddat
from itcc.molecule import read, write, molecule
from itcc.core.frame import parseframe

def dmddat2mtxyz(dmddatfile, molfile, ofile, select_frames=None):
    aDmddat = dmddat.Dmddat(dmddatfile)
    mol = read.readxyz(molfile)

    if select_frames is None:
        select_frames = range(aDmddat.framenum)

    for frame_idx in select_frames:
        aDmddat.seek_frame(frame_idx)
        frame = aDmddat.next().coords
        for i in range(len(frame)):
            mol.coords[i] = molecule.CoordType(frame[i])
        write.writexyz(mol, ofile, comment = 'frame: %i' % (frame_idx+1))

def main():
    import sys
    from optparse import OptionParser

    usage = "usage: %prog [-h|options] dmddatfname molfname"
    parser = OptionParser(usage)
    parser.add_option(
    	"-f", "--frame", dest='frame_str',
	default=None,
	help="select frame, " \
             "format is 'begin[-end[/step]](,begin[-end[/step]])*', " \
             "for example '-f 2-40/3,71-91/2'")
    (options, args) = parser.parse_args()

    frame = parseframe(options.frame_str)

    if len(args) != 2:
        parser.error("incorrect number of arguments")

    dmddat2mtxyz(file(args[0]), file(args[1]), sys.stdout, frame)


if __name__ == '__main__':
    main()
