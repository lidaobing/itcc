# $Id$

__revision__ = '$Rev$'

import os.path
import shutil

def backup(ifname):
    if not os.path.exists(ifname):
        return
    idx = 1
    while True:
        newfname = '%s.%i.bak' % (ifname, idx)
        if not os.path.exists(newfname):
            break
        else:
            idx += 1
    shutil.copy(ifname, newfname)
