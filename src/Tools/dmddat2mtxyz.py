# $Id$

__revision__ = '$Rev$'

from itcc.Tools import dmddat
from itcc.Molecule import read, write, molecule

def parseframe(frame_str):
    if frame_str is None:
        return None
    frame = []
    for range_ in frame_str.split(','):
        nodes = [int(x)-1 for x in range_.split('-')]
        assert len(nodes) in (1,2)
        if len(nodes) == 1:
            frame.append(nodes[0])
        else:
            assert nodes[0] < nodes[1]
            frame.extend(range(nodes[0], nodes[1]+1))
    return tuple(frame)

def dmddat2mtxyz(dmddatfname, molfname, select_frames=None):
    aDmddat = dmddat.Dmddat(file(dmddatfname))
    mol = read.readxyz(file(molfname))

    if select_frames is None:
        select_frames = range(aDmddat.framenum)

    frames = tuple(aDmddat)
    for select_frame in select_frames:
        frame = frames[select_frame]
        assert len(frame) == len(mol)
        for i in range(len(frame)):
            mol.coords[i] = molecule.CoordType(frame[i])
        write.writexyz(mol, comment = 'frame: %i' % (select_frame+1))

def main():
    from optparse import OptionParser

    usage = "usage: %prog [-h|options] dmddatfname molfname"
    parser = OptionParser(usage)
    parser.add_option("-f", "--frame", dest='frame_str',
                      default=None, help="select frame, for example '-f 2-4,7-9'")
    (options, args) = parser.parse_args()

    frame = parseframe(options.frame_str)

    if len(args) != 2:
        parser.error("incorrect number of arguments")

    dmddat2mtxyz(args[0], args[1], frame)


if __name__ == '__main__':
    main()
