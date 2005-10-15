# $Id$

__revision__ = '$Rev$'

from itcc.Tools import dmddat
from itcc.Molecule import read, write, molecule

def parseframe(frame_str):
    if frame_str is None:
        return None
    frame = []
    for range_ in frame_str.split(','):
        step = 1
        if '/' in range_:
            range_, step = tuple(range_.split('-'))
            step = int(step)
        if '-' in range_:
            begin, end = tuple([int(x) - 1 for x in range_.split('-')])
        else:
            begin = int(range_) - 1
            end = begin+1

        frame.extend(range(begin, end, step))
    frame.sort()
    return tuple(frame)

def dmddat2mtxyz(dmddatfname, molfname, select_frames=None):
    aDmddat = dmddat.Dmddat(file(dmddatfname))
    mol = read.readxyz(file(molfname))

    if select_frames is None:
        select_frames = range(aDmddat.framenum)

    for idx, frame in enumerate(aDmddat):
        if idx in select_frames:
            assert len(frame) == len(mol)
            for i in range(len(frame)):
                mol.coords[i] = molecule.CoordType(frame[i])
            write.writexyz(mol, comment = 'frame: %i' % (idx+1))
            if idx == max(select_frames):
                break

def main():
    from optparse import OptionParser

    usage = "usage: %prog [-h|options] dmddatfname molfname"
    parser = OptionParser(usage)
    parser.add_option("-f", "--frame", dest='frame_str',
                      default=None, help="select frame, for example '-f 2-40/3,71-91/2'")
    (options, args) = parser.parse_args()

    frame = parseframe(options.frame_str)

    if len(args) != 2:
        parser.error("incorrect number of arguments")

    dmddat2mtxyz(args[0], args[1], frame)


if __name__ == '__main__':
    main()
