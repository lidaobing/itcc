# $Id$

__revision__ = '$Rev$'

import struct

class Frame:
    def __init__(self, time, coords):
        self.time = time
        self.coords = coords

class Dmddat:
    def __init__(self, ifile):
        self.ifile = ifile
        header_fmt = "=LLLLLLLLLLLLLLLL"
        assert struct.calcsize(header_fmt) == 64
        header_str = ifile.read(struct.calcsize(header_fmt))
        header = struct.unpack(header_fmt, header_str)
        self.beadnum = header[0]
        self.framenum = header[1]
        self.boxsize = tuple([float(x)/1000.0 for x in header[2:5]])
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

    def __iter__(self):
        return self

