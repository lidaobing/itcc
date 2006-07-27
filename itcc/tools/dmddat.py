# $Id$

__revision__ = '$Rev$'

import struct

class Frame:
    def __init__(self, time, coords):
        self.time = time
        self.coords = coords

class Dmddat:
    header_fmt = "=LLLLLLLLLLLLLLLL"
    def __init__(self, ifile):
        self.ifile = ifile
        assert struct.calcsize(self.header_fmt) == 64
        header_str = ifile.read(struct.calcsize(self.header_fmt))
        self.header = struct.unpack(self.header_fmt, header_str)
        header = self.header
        self.version = header[0]
        assert self.version == 2
        self.beadnum = header[1]
        self.framenum = header[2]
        self.boxsize = tuple([float(x)/1000.0 for x in header[3:6]])
        self.nextframe = 0

    def next(self):
        if self.nextframe >= self.framenum:
            raise StopIteration
        self.nextframe += 1

        result = []

        time_fmt = "d"
        time = struct.unpack(time_fmt,
                             self.ifile.read(struct.calcsize(time_fmt)))[0]

        for _ in range(self.beadnum):
            coord_fmt = "=lll"
            assert struct.calcsize(coord_fmt) == 12
            coord_str = self.ifile.read(struct.calcsize(coord_fmt))
            coord = struct.unpack(coord_fmt, coord_str)
            result.append(tuple([float(x)/1000.0 for x in coord]))
        return Frame(time, tuple(result))

    def seek_frame(self, frame_idx):
        header_size = 64
        frame_size = struct.calcsize("d") + struct.calcsize("=lll") * self.beadnum
        self.ifile.seek(header_size + frame_size * frame_idx)

    def __iter__(self):
        return self

