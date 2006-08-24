#!/bin/sh

set -e

PYTHON=python2.4

$PYTHON ../itcc/molecule/dmddat2mtxyz.py -f 1-3/2,4-8/3 dmddat2mtxyz.dmddat dmddat2mtxyz.mol | \
    diff dmddat2mtxyz.ok -

echo OK
