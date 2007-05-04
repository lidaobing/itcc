#!/usr/bin/env python2.4
# $Id$

import os
from setuptools import setup, find_packages
from distutils.core import Extension

def get_ver():
    if os.system('which svnversion > /dev/null') != 0:
        svnversion = 'exported'
    else:
        # some old subversion require use "svnversion ."
        svnversion = os.popen('svnversion .').read().strip()

    version = file('version.in').read().strip()
    
    if svnversion == 'exported':
        return version
    else:
        return "%s.dev-r%s" % (version, svnversion.split(':')[-1])

__version__ = None
if os.path.exists('itcc/__init__.py'):
    execfile('itcc/__init__.py')

if __version__ != get_ver():
    __version__ = get_ver()
    file('itcc/__init__.py', 'w').write("__version__ = '%s'\n" % __version__)

__revision__ = '$Rev$'

ext_modules = [Extension("itcc.tools.ctools", ["itcc/tools/ctools.c"]),
               Extension("itcc.tools.cpptools",
                         ["itcc/tools/cpptools.cpp"],
                         depends=['itcc/tools/vector.hpp']),
               Extension('itcc.molecule._rmsd',
                         ['itcc/molecule/_rmsd.cpp'],
                         libraries=['lapack'])
               ]

setup(
    name="itcc",
    version=__version__,
    author='LI Daobing',
    author_email='lidaobing@gmail.com',
    url='http://www.chemgen.szpku.edu.cn',
    packages = find_packages(),
    ext_modules = ext_modules,
    data_files = [('/etc/bash_completion.d', ['bash_completion/itcc']),
        ],
    test_suite = 'itcc.tests',
    entry_points = {
        'console_scripts': [
            'itcc = itcc.itcc_main:main',
            'itcc-makecyclicalkane = itcc.tools.makecyclicalkane:main',
            'itcc-stats = itcc.tools.stats:main',
            'itcc-calcangle = itcc.tools.calcangle:main',
            'itcc-ene2agr = itcc.tools.ene2agr:main',
            'itcc-enestep2countstep = itcc.tools.enestep2countstep:main',
            'itcc-random-protein-input = itcc.tools.random_protein_input:main',
            'itcc-verifyloop = itcc.tools.verifyloop:main',
            'itcc-mirrormol = itcc.molecule.utils:mirrormol',
            'itcc-printbonds = itcc.molecule.utils:printbonds',
            'itcc-detailcmp = itcc.molecule.utils:detailcmp',
            'itcc-caflisch = itcc.ccs2.solvent_caflisch:main',
            'itcc-loopdetect = itcc.ccs2.detectloop:main',
        ]
    },
    include_package_data = True

#    install_requires = ['numpy', 'Scientific']
)
