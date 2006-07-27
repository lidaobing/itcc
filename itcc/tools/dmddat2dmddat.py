# $Id$
__revision__ = '$Rev$'

import struct
import sys
from itcc.tools.frame import parseframe
from itcc.tools.dmddat import Dmddat

def dmddat2dmddat(ifile, ofile, frames):
    aDmddat = Dmddat(ifile)
    frames = tuple(frames)
    header = list(aDmddat.header)
    header[2] = len(frames)
    header_str = struct.pack(Dmddat.header_fmt, *header)
    ofile.write(header_str)

    headersize = 64
    framesize = struct.calcsize("d") + 12 * aDmddat.beadnum

    for frame in frames:
        ifile.seek(headersize + framesize * frame)
        ofile.write(ifile.read(framesize))

def main():
    from optparse import OptionParser

    usage = "usage: %prog [-h|options] dmddatfname"
    parser = OptionParser(usage)
    parser.add_option(
        "-f", "--frame", dest='frame_str', default=None,
	help="select frame, " \
             "format is 'begin[-end[/step]](,begin[-end[/step]])*', " \
             "for example '-f 2-40/3,71-91/2'")
    parser.add_option(
        "-F", "--framefile", dest='frame_file', default=None,
	help="read frame from file")
    parser.add_option(
        '-o', '--output', dest='output_fname', default=None,
        help="output filename")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("incorrect number of arguments")

    if args[0] == '-':
        ifile = sys.stdin
    else:
        ifile = file(args[0])

    if options.frame_str is not None:
        frame = parseframe(options.frame_str)
    elif options.frame_file is not None:
        frame = parseframe(file(options.frame_file).read())
    else:
        return

    if options.output_fname is None:
        ofile = sys.stdout
    else:
        ofile = file(options.output_fname, 'w')

    dmddat2dmddat(ifile, ofile, frame)

if __name__ == '__main__':
    main()
