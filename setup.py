#!/usr/bin/env python2.4
# $Id$

import os
import numpy
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

__version__ = get_ver()

new_init_py = file('itcc/__init__.py.in').read()
new_init_py = new_init_py.replace('@VERSION@', __version__)

if not os.path.exists('itcc/__init__.py') \
        or file('itcc/__init__.py').read() != new_init_py:
            file('itcc/__init__.py', 'w').write(new_init_py)

__revision__ = '$Rev$'


incdirs = [numpy.get_include()]
ext_modules = [Extension("itcc.core.ctools", ["itcc/core/ctools.c"]),
               Extension("itcc.tools.cpptools",
                         ["itcc/tools/cpptools.cpp"],
                         depends=['itcc/tools/vector.hpp']),
               Extension('itcc.molecule._rmsd',
                         ['itcc/molecule/_rmsd.cpp'],
                         include_dirs = incdirs,
                         libraries=['lapack']),
#               Extension('itcc.mopac._mopac',
#                         ['itcc/mopac/_mopac.cpp'],
#                         libraries=['mopac7', 'g2c', 'boost_python-mt'])
               ]

setup(
    name="itcc",
    version=__version__,
    author='LI Daobing',
    author_email='lidaobing@gmail.com',
    url='http://www.chemgen.szpku.edu.cn',
    packages = find_packages(),
    ext_modules = ext_modules,
    test_suite = 'tests',
    entry_points = {
        'console_scripts': [
            'itcc = itcc.itcc_main:main',
            'itcc-makecyclicalkane = itcc.tools.makecyclicalkane:main',
            'itcc-stats = itcc.tools.stats:main',
            'itcc-calcangle = itcc.tools.calcangle:main',
            'itcc-ene2agr = itcc.tools.ene2agr:main',
            'itcc-enestep2countstep = itcc.tools.enestep2countstep:main',
            'itcc-random-protein-input = itcc.tools.random_protein_input:main',
            'itcc-loopverify = itcc.tools.verifyloop:main',
            'itcc-count = itcc.tools.count:main',
            'itcc-mirrormol = itcc.molecule.utils:mirrormol',
            'itcc-printbonds = itcc.molecule.utils:printbonds',
            'itcc-detailcmp = itcc.molecule.utils:detailcmp',
            'itcc-rg = itcc.molecule.utils:rg',
            'itcc-pyramid-check = itcc.molecule.utils:pyramid_check',
            'itcc-loopdetect = itcc.ccs2.detectloop:main',
            'itcc-out2ene = itcc.tools.out2ene:main',
            'itcc-out2arch = itcc.tools.out2arch:main',
            'itcc-xyz2gjf = itcc.tools.xyz2gjf:main',
            'itcc-gjf2xyz = itcc.molecule.gjf2xyz:main',
            'itcc-optimizes = itcc.tinker.optimizes:main',
            'itcc-xyz2gro = itcc.tools.xyz2gro:main',
            'itcc-xyz2pdb = itcc.molecule.xyz2pdb:main',
            'itcc-chiral = itcc.molecule.chiral:main',
            'itcc-confsearch = itcc.ccs2.confsearch:main',
            'itcc-catordiff = itcc.ccs2.catordiff:main',
            'itcc-detectloop = itcc.ccs2.detectloop:main',
            'itcc-dmddummy = itcc.tools.dmddummy:main',
            'itcc-scalexyz = itcc.tools.scalexyz:main',
            'itcc-columnmean = itcc.tools.columnmean:main',
            'itcc-almostequaldiff = itcc.tools.almostequaldiff:main',
            'itcc-shake = itcc.tools.shake:main',
            'itcc-mtxyzstat = itcc.tools.mtxyzstat:main',
            'itcc-mol2top = itcc.molecule.mol2top:main',
            'itcc-mtxyzrg = itcc.tools.mtxyzrg:main',
            'itcc-sumxyz = itcc.tools.sumxyz:main',
            'itcc-parmeval = itcc.torsionfit.parmeval:main',
            'itcc-dmddat_fix = itcc.tools.dmddat_fix:main',
            'itcc-onecolumn = itcc.tools.onecolumn:main',
            'itcc-settype = itcc.molecule.settype:main',
            'itcc-sumparam = itcc.tools.sumparam:main',
            'itcc-removepbc = itcc.molecule.removepbc:main',
            'itcc-dmddat2dmddat = itcc.tools.dmddat2dmddat:main',
            'itcc-parmfit = itcc.torsionfit.parmfit:main',
            'itcc-cmpxyztop = itcc.molecule.cmpxyztop:main',
            'itcc-simpparam = itcc.tinker.simpparam:main',
            'itcc-tor2freeene = itcc.tools.tor2freeene:main',
            'itcc-rmsd = itcc.molecule.rmsd:main_rmsd',
            'itcc-rmsd2 = itcc.molecule.rmsd:main_rmsd2',
            'itcc-dmddat2mtxyz = itcc.tools.dmddat2mtxyz:main',
            'itcc-printefit = itcc.torsionfit.printefit:main',
            'itcc-constrain = itcc.tinker.constrain:main',
            'itcc-loop2looptor = itcc.tools.loop2looptor:main',
            'itcc-idx-verify = itcc.tools.idx_verify:main',
            'itcc-molcenter = itcc.tools.molcenter:main',
            'itcc-rotate-to = itcc.tools.rotate_to:main',
            'itcc-histogram = itcc.tools.histogram:main',
            'itcc-tordiff = itcc.tools.tordiff:main',
        ]
    },
    include_package_data = True,
    classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'License :: Other/Proprietary License',
            'Natural Language :: English',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Programming Language :: C',
            'Programming Language :: C++',
            'Topic :: Scientific/Engineering :: Chemistry',
            ],
    license = 'Other/Proprietary License',
#    install_requires = ['numpy', 'Scientific']
)
