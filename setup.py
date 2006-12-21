#!/usr/bin/env python2.4
# $Id$
from distutils.core import setup, Extension
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
    ofile.write("__version__ = '%s (SVN%s)'\n" % 
                  (file('version.in').read().strip(),
                   svnversion))
ofile.close()

import itcc

__revision__ = '$Rev$'

version = itcc.__version__
scripts = ['itcc/scripts/itcc']

ext_modules=[Extension("itcc.tools.ctools", ["itcc/tools/ctools.c"]),
             Extension("itcc.tools.cpptools",
                       ["itcc/tools/cpptools.cpp"],
                       depends=['itcc/tools/vector.hpp']),
             Extension('itcc.vools.vector',
                       ['itcc/tools/vector.cpp'],
                       depends=['itcc/tools/vector.hpp'],
                       libraries=['boost_python']),
             Extension('itcc.molecule._rmsd',
                       ['itcc/molecule/_rmsd.cpp'],
                       libraries=['lapack'])
             ]


setup(name="itcc",
      version=version,
      author='LI Daobing',
      author_email='lidaobing@gmail.com',
      url='http://219.223.205.41/~lidb',
      package_dir={'itcc':'itcc',
                   'itcc.ccs2':'itcc/ccs2',
                   'itcc.molecule':'itcc/molecule',
                   'itcc.tinker':'itcc/tinker',
                   'itcc.tools':'itcc/tools',
                   'itcc.torsionfit': 'itcc/torsionfit'},
      packages=["itcc",
                'itcc.ccs2',
                'itcc.molecule',
                'itcc.tinker',
                'itcc.tools',
                'itcc.torsionfit'],
      ext_modules = ext_modules,
      scripts=scripts,
      data_files = [('/etc/bash_completion.d', ['bash_completion/itcc'])]
      )

