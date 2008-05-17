#!/usr/bin/env python

import os
import sys
import glob
from setuptools import setup, find_packages
from distutils.core import Extension

name = 'itcc'
version = '0.9.2'
description = 'my collection of scripts on computational chemistry'
author = 'LI Daobing'
author_email = 'lidaobing@gmail.com'
url = 'http://pypi.python.org/pypi/itcc'
packages = [x for x in find_packages() if x.startswith('itcc')]
scripts = [x for x in glob.glob('scripts/*') if not x.endswith('~')]

ext_modules = [Extension("itcc.core.ctools", ["ext/itcc-core-ctools.c"]),
               Extension("itcc.tools.cpptools",
                         ["ext/itcc-tools-cpptools.cpp"],
                         depends=['ext/vector.hpp']),
               Extension('itcc.molecule._rmsd',
                         ['ext/itcc-molecule-_rmsd.cpp'],
                         libraries=['lapack']),
#               Extension('itcc.mopac._mopac',
#                         ['itcc/mopac/_mopac.cpp'],
#                         libraries=['mopac7', 'g2c', 'boost_python-mt'])
               ]

py_modules = []
if sys.version_info[:2] == (2, 3):
    py_modules.append('subprocess')
test_suite = 'tests'
entry_points = {
    'console_scripts': [
        'itcc = itcc.itcc_main:main',
        'itcc-addmethyl = itcc.tools.addmethyl:main',
        'itcc-almostequaldiff = itcc.tools.almostequaldiff:main',
        'itcc-autodock-charge-bury = itcc.tools.autodock_charge_bury:main',
        'itcc-autodock-charge-bury2 = itcc.tools.autodock_charge_bury2:main',
        'itcc-ball = itcc.tools.ball:main',
        'itcc-calcangle = itcc.tools.calcangle:main',
        'itcc-catordiff = itcc.ccs2.catordiff:main',
        'itcc-ccslog2enestep = itcc.tools.ccslog2enestep:main',
        'itcc-ccslog2major = itcc.tools.ccslog2major:main',
        'itcc-chiral = itcc.molecule.chiral:main',
        'itcc-cmpxyztop = itcc.molecule.cmpxyztop:main',
        'itcc-columnmean = itcc.tools.columnmean:main',
        'itcc-confsearch = itcc.ccs2.confsearch:main',
        'itcc-constrain = itcc.tinker.constrain:main',
        'itcc-count = itcc.tools.count:main',
        'itcc-detailcmp = itcc.molecule.utils:detailcmp',
        'itcc-detectloop = itcc.ccs2.detectloop:main',
        'itcc-dlg-stat = itcc.tools.dlg_stat:main',
        'itcc-dmddat2dmddat = itcc.tools.dmddat2dmddat:main',
        'itcc-dmddat2mtxyz = itcc.tools.dmddat2mtxyz:main',
        'itcc-dmddat_fix = itcc.tools.dmddat_fix:main',
        'itcc-dmddummy = itcc.tools.dmddummy:main',
        'itcc-ene2agr = itcc.tools.ene2agr:main',
        'itcc-enestep2countstep = itcc.tools.enestep2countstep:main',
        'itcc-findneighbour = itcc.ccs2.confsearch2:main',
        'itcc-floatformat = itcc.tools.floatformat:main',
        'itcc-gjf2xyz = itcc.molecule.gjf2xyz:main',
        'itcc-histogram = itcc.tools.histogram:main',
        'itcc-idx-verify = itcc.tools.idx_verify:main',
        'itcc-loop2looptor = itcc.tools.loop2looptor:main',
        'itcc-loopdetect = itcc.ccs2.detectloop:main',
        'itcc-loopverify = itcc.tools.verifyloop:main',
        'itcc-makecyclicalkane = itcc.tools.makecyclicalkane:main',
        'itcc-mirrormol = itcc.molecule.utils:mirrormol',
        'itcc-mol2top = itcc.molecule.mol2tor:main',
        'itcc-mol2tor = itcc.molecule.mol2tor:main',
        'itcc-molcenter = itcc.tools.molcenter:main',
        'itcc-moldiff = itcc.tools.moldiff:main',
        'itcc-mtxyz2txyz = itcc.tools.mtxyz2txyz:main',
        'itcc-mtxyzrg = itcc.tools.mtxyzrg:main',
        'itcc-mtxyzstat = itcc.tools.mtxyzstat:main',
        'itcc-multi = itcc.tools.multi:main',
        'itcc-omega = itcc.tools.omega:main',
        'itcc-omega2restrain = itcc.tools.omega2restrain:main',
        'itcc-onecolumn = itcc.tools.onecolumn:main',
        'itcc-optimizes = itcc.tinker.optimizes:main',
        'itcc-out2arch = itcc.tools.out2arch:main',
        'itcc-out2ene = itcc.tools.out2ene:main',
        'itcc-parmeval = itcc.torsionfit.parmeval:main',
        'itcc-parmfit = itcc.torsionfit.parmfit:main',
        'itcc-pdbqchargeshift = itcc.tools.pdbqchargeshift:main',
        'itcc-pdbqchargesum = itcc.tools.pdbqcharge:main',
        'itcc-pdbq-large-charge = itcc.tools.pdbq_large_charge:main',
        'itcc-printbonds = itcc.molecule.utils:printbonds',
        'itcc-printefit = itcc.torsionfit.printefit:main',
        'itcc-pyramid-check = itcc.molecule.utils:pyramid_check',
        'itcc-random-protein-input = itcc.tools.random_protein_input:main',
        'itcc-ranlog2enestep = itcc.tools.ranlog2enestep:main',
        'itcc-relative = itcc.tools.relative:main',
        'itcc-removepbc = itcc.molecule.removepbc:main',
        'itcc-rg = itcc.molecule.utils:rg',
        'itcc-rmsd = itcc.molecule.rmsd:main_rmsd',
        'itcc-rmsd2 = itcc.molecule.rmsd:main_rmsd2',
        'itcc-rotate-to = itcc.tools.rotate_to:main',
        'itcc-scalexyz = itcc.tools.scalexyz:main',
        'itcc-scanlog2enestep = itcc.tools.scanlog2enestep:main',
        'itcc-scanlog2idxene = itcc.tools.scanlog2idxene:main',
        'itcc-settype = itcc.molecule.settype:main',
        'itcc-shake = itcc.tools.shake:main',
        'itcc-simpparam = itcc.tinker.simpparam:main',
        'itcc-stats = itcc.tools.stats:main',
        'itcc-sumparam = itcc.tools.sumparam:main',
        'itcc-sumxyz = itcc.tools.sumxyz:main',
        'itcc-tor2freeene = itcc.tools.tor2freeene:main',
        'itcc-tor2omega = itcc.tools.tor2omega:main',
        'itcc-tordiff = itcc.tools.tordiff:main',
        'itcc-xyz2gjf = itcc.tools.xyz2gjf:main',
        'itcc-xyz2gro = itcc.tools.xyz2gro:main',
        'itcc-xyz2pdb = itcc.molecule.xyz2pdb:main',
    ]
}
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
        ]
license_ = 'OSI Approved :: GNU General Public License (GPL)'

def main():
    setup(
        name=name,
        version=version,
        description=description,
        author=author,
        author_email=author_email,
        url=url,
        packages = packages,
        ext_modules = ext_modules,
        py_modules = py_modules,
        test_suite = test_suite,
        entry_points = entry_points,
        include_package_data = False,
        classifiers = classifiers,
        license = license_,
        scripts = scripts,
    )

if __name__ == '__main__':
    main()

