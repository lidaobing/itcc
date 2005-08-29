#!/bin/sh

set -ev

python ../src/Tools/mol2top.py cycC17.1.xyz | \
    diff mol2top.result -

echo OK
