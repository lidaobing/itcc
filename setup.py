import glob
from distutils.core import setup, Extension

__revision__ = '$Rev$'

scripts = glob.glob('src/scripts/*.py')

setup(name="itcc",
      version="0.2.1",
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
      ext_modules=[Extension("itcc.Tools.ctools", ["src/Tools/ctools.c"]),
                   Extension("itcc.Tools.cpptools",
                       ["src/Tools/cpptools.cpp"])],
      scripts=scripts
      )

