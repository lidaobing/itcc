# $Id$
# $Log: parmeval.py,v $
# Revision 1.3  2004/03/07 10:49:10  nichloas
# delete `from os import ...'
#
# Revision 1.2  2004/02/04 06:14:28  nichloas
# *** empty log message ***
#
# Revision 1.1.1.1  2003/11/20 06:12:42  nichloas
# Initial version
#
# Revision 1.1.1.1  2003/11/20 05:56:49  nichloas
# initial version
#

import os

def tmpmerge(param, ifname, ofname):
    """
    merge param to template file. output to another file.
    """
    ifile = file(ifname, 'r')
    idata = ifile.read()
    ifile.close()

    odata = idata % tuple(param)

    ofile = file(ofname, 'w+')
    ofile.write(odata)
    ofile.close()

def findxyz():
    return [x for x in os.listdir(os.getcwd()) if os.path.splitext(x) == '.xyz']

def calene(fname):
    command = 'optimize %s 0.01' % fname
    out = os.popen(command)
    lines = out.readlines()
    out.close()

    command = 'rm -f %s_2' % fname
    os.system(command)

    for x in lines:
        if x.find('Final Function Value') != -1:
            x = x.split()
            result = float(x[-1])
            return result
    return None


class Parmeval:
    def __init__(self):
        self.template = 'tinker.tmpl'
        self.filelist = findxyz
        self.reference = []

    
    def parmeval(self,param):
        tmpmerge(param, self.template, 'tinker.key')
        

        
    
    
    
