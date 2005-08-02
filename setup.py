# $Id$
from distutils.core import setup, Extension

__revision__ = '$Rev$'

scripts = ['src/scripts/itcc']

ext_modules=[Extension("itcc.Tools.ctools", ["src/Tools/ctools.c"]),
             Extension("itcc.Tools.cpptools",
                       ["src/Tools/cpptools.cpp"],
                       depends=['src/Tools/Vector.hpp']),
             Extension('itcc.Tools.Vector',
                       ['src/Tools/Vector.cpp'],
                       depends=['src/Tools/Vector.hpp'],
                       libraries=['boost_python']),
             Extension('itcc.Molecule._rmsd',
                       ['src/Molecule/_rmsd.cpp'],
                       libraries=['lapack']),
             ]


setup(name="itcc",
      version="0.2.7",
      author='Li Daobing',
      author_email='lidaobing@gmail.com',
      package_dir={'itcc':'src',
                   'itcc.CCS2':'src/CCS2',
                   'itcc.Molecule':'src/Molecule',
                   'itcc.Tinker':'src/Tinker',
                   'itcc.Tools':'src/Tools',
                   'itcc.Torsionfit': 'src/Torsionfit'},
      packages=["itcc",
                'itcc.CCS2',
                'itcc.Molecule',
                'itcc.Tinker',
                'itcc.Tools',
                'itcc.Torsionfit'],
      ext_modules = ext_modules,
      scripts=scripts
      )

