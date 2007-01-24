#!/usr/bin/env python2.4
# $Id$

from setuptools import setup, find_packages
from distutils.core import Extension
import os

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
#    install_requires = ['Numeric', 'Scientific']
)
