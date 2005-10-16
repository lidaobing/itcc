#!/bin/sh

set -ev

python ../itcc/Tools/mol2top.py mol2top.xyz | \
    diff mol2top.ok -

python ../itcc/Tools/onecolumn.py onecolumn.xyz | \
    diff onecolumn.ok -

python ../itcc/Tools/dmddat2mtxyz.py -f 1-3/2,4-8/3 dmddat2mtxyz.dmddat dmddat2mtxyz.mol | \
    diff dmddat2mtxyz.ok -

echo OK
