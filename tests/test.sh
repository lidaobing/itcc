#!/bin/sh

set -ev

python ../itcc/Tools/mol2top.py mol2top.xyz | \
    diff mol2top.ok -

python ../itcc/Tools/onecolumn.py onecolumn.xyz | \
    diff onecolumn.ok -

python ../itcc/Tools/dmddat2mtxyz.py -f 1-3/2,4-8/3 dmddat2mtxyz.dmddat dmddat2mtxyz.mol | \
    diff dmddat2mtxyz.ok -

python ../itcc/Tools/dmddat2xtc.py dmddat2xtc.dmddat dmddat2xtc.tmp.xtc
cmp dmddat2xtc.tmp.xtc dmddat2xtc.`uname -m`.ok.xtc
rm -f dmddat2xtc.tmp.xtc

echo OK
