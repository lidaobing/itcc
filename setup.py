# $Id$
from distutils.core import setup, Extension
import itcc

__revision__ = '$Rev$'

version = itcc.__version__
scripts = ['itcc/scripts/itcc']

ext_modules=[Extension("itcc.Tools.ctools", ["itcc/Tools/ctools.c"]),
             Extension("itcc.Tools.cpptools",
                       ["itcc/Tools/cpptools.cpp"],
                       depends=['itcc/Tools/Vector.hpp']),
             Extension('itcc.Tools.Vector',
                       ['itcc/Tools/Vector.cpp'],
                       depends=['itcc/Tools/Vector.hpp'],
                       libraries=['boost_python']),
             Extension('itcc.Molecule._rmsd',
                       ['itcc/Molecule/_rmsd.cpp'],
                       libraries=['lapack']),
             Extension('itcc.Tools._gmx_xtcio',
                       ['itcc/Tools/_gmx_xtcio.c'],
                       include_dirs=["/usr/include/gromacs"],
                       libraries=['gmx'])
             ]


setup(name="itcc",
      version=version,
      author='LI Daobing',
      author_email='lidaobing@gmail.com',
      package_dir={'itcc':'itcc',
                   'itcc.CCS2':'itcc/CCS2',
                   'itcc.Molecule':'itcc/Molecule',
                   'itcc.Tinker':'itcc/Tinker',
                   'itcc.Tools':'itcc/Tools',
                   'itcc.Torsionfit': 'itcc/Torsionfit'},
      packages=["itcc",
                'itcc.CCS2',
                'itcc.Molecule',
                'itcc.Tinker',
                'itcc.Tools',
                'itcc.Torsionfit'],
      ext_modules = ext_modules,
      scripts=scripts,
      )

