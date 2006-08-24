#!/bin/sh

set -e

PYTHON=python2.4

$PYTHON ../itcc/molecule/mol2top.py mol2top.xyz | \
    diff mol2top.ok -

$PYTHON ../itcc/tools/onecolumn.py onecolumn.xyz | \
    diff onecolumn.ok -

$PYTHON ../itcc/molecule/dmddat2mtxyz.py -f 1-3/2,4-8/3 dmddat2mtxyz.dmddat dmddat2mtxyz.mol | \
    diff dmddat2mtxyz.ok -

echo OK
