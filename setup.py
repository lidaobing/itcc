from distutils.core import setup, Extension

setup(name="itcc",
      version="0.0.1",
      author='Li Daobing',
      author_email='lidaobing@gmail.com',
      package_dir={'itcc':'src',
                   'itcc.CCS2':'src/CCS2',
                   'itcc.Molecule':'src/Molecule',
                   'itcc.Tinker':'src/Tinker',
                   'itcc.Tools':'src/Tools'},
      packages=["itcc",
                'itcc.CCS2',
                'itcc.Molecule',
                'itcc.Tinker',
                'itcc.Tools'],
      ext_modules=[Extension("itcc.Tools.ctools", ["src/Tools/ctools.c"]),
                   Extension("itcc.Tools.cpptools",
                       ["src/Tools/cpptools.cpp"])],
      scripts=['src/scripts/settype.py']
      )

