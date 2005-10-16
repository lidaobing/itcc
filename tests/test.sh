#!/bin/sh

set -ev

python ../itcc/Tools/mol2top.py cycC17.1.xyz | \
    diff mol2top.result -

python ../itcc/Tools/onecolumn.py cycC17.1.xyz | \
    diff onecolumn.result -

echo OK
