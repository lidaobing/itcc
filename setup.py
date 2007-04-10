#!/usr/bin/env python2.4
# $Id$

from setuptools import setup, find_packages
from distutils.core import Extension
import os

if os.system('which svnversion > /dev/null') != 0:
    svnversion = 'exported'
else:
    svnversion = os.popen('svnversion .').read().strip()

ofile = file('itcc/__init__.py', 'w')
if svnversion == 'exported':
    ofile.write("__version__ = '%s'\n" %
                  file('version.in').read().strip())
else:
    ofile.write("__version__ = '%s.dev-r%s'\n" % 
                  (file('version.in').read().strip(),
                      svnversion.split(':')[-1]))
ofile.close()

import itcc

__revision__ = '$Rev$'

version = itcc.__version__
scripts = ['itcc/scripts/itcc']

ext_modules=[Extension("itcc.tools.ctools", ["itcc/tools/ctools.c"]),
             Extension("itcc.tools.cpptools",
                       ["itcc/tools/cpptools.cpp"],
                       depends=['itcc/tools/vector.hpp']),
             Extension('itcc.tools.vector',
                       ['itcc/tools/vector.cpp'],
                       depends=['itcc/tools/vector.hpp'],
                       libraries=['boost_python']),
             Extension('itcc.molecule._rmsd',
                       ['itcc/molecule/_rmsd.cpp'],
                       libraries=['lapack'])
             ]

setup(
    name="itcc",
    version=version,
    author='LI Daobing',
    author_email='lidaobing@gmail.com',
    url='http://www.chemgen.szpku.edu.cn',
    packages = find_packages(),
    ext_modules = ext_modules,
    scripts=scripts,
    data_files = [('/etc/bash_completion.d', ['bash_completion/itcc'])],
    test_suite = 'itcc.tests',
    entry_points = {
        'console_scripts': [
            'itcc-stats = itcc.tools.stats:main',
            'itcc-mirrormol = itcc.molecule.utils:mirrormol'
        ]
    }
#    install_requires = ['numpy', 'Scientific']
)
