# $Id$

import errno

class IgnoreEpipe(object):
    def __init__(self, ofile):
        self.ofile = ofile
    
    def write(self, str):
        try:
            self.ofile.write(str)
        except IOError, e:
            if e.errno != errno.EPIPE:
                raise

    def flush(self):
        try:
            self.ofile.flush()
        except IOError, e:
            if e.errno != errno.EPIPE:
                raise
