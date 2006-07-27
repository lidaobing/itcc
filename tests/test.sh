#!/bin/sh

set -e

PYTHON=python2.4

$PYTHON ../itcc/tools/mol2top.py mol2top.xyz | \
    diff mol2top.ok -

$PYTHON ../itcc/tools/onecolumn.py onecolumn.xyz | \
    diff onecolumn.ok -

$PYTHON ../itcc/tools/dmddat2mtxyz.py -f 1-3/2,4-8/3 dmddat2mtxyz.dmddat dmddat2mtxyz.mol | \
    diff dmddat2mtxyz.ok -

$PYTHON ../itcc/tools/xyz2pdb.py xyz2pdb.xyz - \
    | diff xyz2pdb.ok -

echo OK
