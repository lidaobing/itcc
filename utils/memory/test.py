#!/usr/bin/env python

import os

from itcc.molecule import read

mol = read.readxyz(file("cycA12.xyz"))

os.system("ps -p %s -o rss" % os.getpid())

b = []
for i in range(1000):
    b.append(mol.copy())

os.system("ps -p %s -o rss" % os.getpid())

del b
b = []
for i in range(1000):
    b.append(mol.coords.copy())
os.system("ps -p %s -o rss" % os.getpid())

del b
os.system("ps -p %s -o rss" % os.getpid())

