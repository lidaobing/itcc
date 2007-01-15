# $Id$

import sys
import pprint

from itcc.molecule import read
from itcc.ccs2 import loopdetect, loopclosure, peptide

def main():
    mol = read.readxyz(file(sys.argv[1]))
    loop  = loopdetect.loopdetect(mol)[1][0]
    loopc = loopclosure.LoopClosure()

    shakedata = loopclosure.getshakedata(mol, loop)
    loopc.shakedata = shakedata
    loopc.forcefield = "oplsaa"
    loopc.log_level = 0

    for r6 in peptide.Peptide(mol).getr6s(loop):
        for mol, ene in loopc.findneighbor(mol, r6):
            print ene

if __name__ == '__main__':
    main()
