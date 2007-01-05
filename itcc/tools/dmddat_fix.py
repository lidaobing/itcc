# $Id$

__revision__ = '$Rev$'

import sys
import struct
import copy
import os.path
from itcc.tools.backup import backup

def get_format_new():
    while True:
        ans = raw_input("please select file format (N)ew/(O)ld, default is new: ")
        if not ans or ans.lower() in ("n", "new"):
            return "new"
        elif ans.lower() in ("o", "old"):
            return "old"
        else:
            continue

def get_format_old():
    while True:
        ans = raw_input("please select file format (N)ew/(O)ld, default is old: ")
        if not ans or ans.lower() in ("o", "old"):
            return "old"
        elif ans.lower() in ("n", "new"):
            return "new"
        else:
            continue

class Olddmddat_Header:
    header_fmt = "=6L40x"
    def __init__(self, ifile):
        header_fmt = self.header_fmt
        assert struct.calcsize(header_fmt) == 64
        header_str = ifile.read(struct.calcsize(header_fmt))
        header = struct.unpack(header_fmt, header_str)

        if header[0] == 2:
            print 'this file seems to be in new format.'
            self.format = get_format_new()
        else:
            print 'this file seems to be in old format.'
            self.format = get_format_old()

        if self.format == 'old':
            self.beadnum = header[0]
            self.framenum = header[1]
            self.boxsize = tuple([float(x)/1000.0 for x in header[2:5]])
        else:
            assert self.format == 'new'
            self.beadnum = header[1]
            self.framenum = header[2]
            self.boxsize = tuple([float(x)/1000.0 for x in header[3:6]])

    def calc_framenum(self, file_size):
        self.framenum = (file_size - struct.calcsize(self.header_fmt)) // self.frame_size()

    def frame_size(self):
        if self.format == 'old':
            return self.beadnum * 3 * 4
        else:
            return self.beadnum * 3 * 4 + 8

    def pack(self):
        if self.format == 'old':
            return struct.pack(self.header_fmt, self.beadnum, self.framenum,
                               int(self.boxsize[0] * 1000),
                               int(self.boxsize[1] * 1000),
                               int(self.boxsize[2] * 1000),
                               0)
        else:
            return struct.pack(self.header_fmt, 2, self.beadnum, self.framenum,
                               int(self.boxsize[0] * 1000),
                               int(self.boxsize[1] * 1000),
                               int(self.boxsize[2] * 1000))

    def __eq__(self, other):
        return self.beadnum == other.beadnum \
                and self.framenum == other.framenum \
                and self.boxsize == other.boxsize

def check_version(header):
    if header.beadnum == 2:
        ans = raw_input("this file sames not to be an olddmddat format, do you want to continue [y/N] ")
        if ans and ans in ["y", "Y"]:
            return
        else:
            sys.exit(0)

def change_beadnum(header):
    ans = raw_input("old beadnum is %i, please input new beadnum, press enter means not change: " % header.beadnum)
    if ans:
        header.beadnum = int(ans)

def change_framenum(header):
    ans = raw_input("old framenum is %i, please input new framenum, press enter means not change, enter 0 means autodetect: " % header.framenum)
    if ans:
        header.framenum = int(ans)

def change_boxsize(header):
    while True:
        ans = raw_input("old boxsize is %s, please input new boxsize, "
                        "enter means not change, seperate by space: " % (header.boxsize,))
        if not ans: return
        try:
            words = ans.split()
            assert len(words) == 3
            header.boxsize = tuple([float(x) for x in words])
            return
        except:
            print 'format error'
            continue

def ask_backup():
    while True:
        ans = raw_input("need backup(Y/n): ")
        if not ans or ans in ['Y', 'y']:
            return True
        elif ans in ['N', 'n']:
            return False
        else:
            print 'illegal input'
            continue
    return False

def ask_change():
    while True:
        ans = raw_input("apply change(Y/n): ")
        if not ans or ans in ['Y', 'y']:
            return True
        elif ans in ['N', 'n']:
            return False
        else:
            print 'illegal input'
            continue
    return False

def olddmddat_fix(ifname):
    ifile = file(ifname, 'r+')
    header = Olddmddat_Header(ifile)

    oldheader = copy.copy(header)
    check_version(header)
    change_beadnum(header)
    change_framenum(header)
    change_boxsize(header)

    if header.framenum == 0:
        header.calc_framenum(os.path.getsize(ifname))

    if oldheader == header:
        print 'nothing is changed.'
        return

    print '%16s%16s%16s' % ('', 'Old', 'New')
    print '%16s%16s%16s' % ('beadnum', oldheader.beadnum, header.beadnum)
    print '%16s%16s%16s' % ('framenum', oldheader.framenum, header.framenum)
    print '%16s%16.2f%16.2f' % ('boxsize.x', oldheader.boxsize[0], header.boxsize[0])
    print '%16s%16.2f%16.2f' % ('boxsize.y', oldheader.boxsize[1], header.boxsize[1])
    print '%16s%16.2f%16.2f' % ('boxsize.z', oldheader.boxsize[2], header.boxsize[2])

    if not ask_change(): return
    if ask_backup():
        print 'backup', ifname,
        backup(ifname)
        print 'Done'
    ifile.seek(0)
    ifile.write(header.pack())
    ifile.close()

def main():
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write("Usage: %s dmddatfname\n" % os.path.basename(sys.argv[0]))
        sys.exit(1)

    olddmddat_fix(sys.argv[1])

if __name__ == '__main__':
    main()

