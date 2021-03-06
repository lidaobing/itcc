itcc NEWS
=========

.. contents::

0.8.2.dev
---------

new scripts
'''''''''''

itcc-stats, itcc-mirrormol, itcc-calcangle, itcc-ene2agr,
itcc-enestep2countstep, itcc-count, itcc-loop2looptor, itcc-idx-verify,
itcc-molcenter, itcc-rotate-to, itcc-tordiff, itcc-relative, itcc-rg,
itcc-pyramid-check, itcc-mtxyz2txyz, itcc-pdbqchargesum, itcc-pdbqchargeshift,
itcc-dlg, itcc-ccslog2enestep

itcc-mol2top rename to itcc-mol2tor.


modified scripts
''''''''''''''''

itcc-confsearch
"""""""""""""""

* add '-c', '-C', '-e' options, these options can provide a method to
  avoid minimize freeze when minimization some weird conformation.
      
* add '--chain' option, support conformational search on a chain. (r641)

* add '--cmptor' option, support specify torsion angles used for
  compare.  (r645)

* add '--chiral', '--achiral', '--head-tail', '--loopstep'

* add '--config'

* add 'tinker_key_file' to config
* add 'min_method' to config

itcc-rmsd
"""""""""

* new "--no-h" option.
* new "--mirror" option.
* support read from stdin.
    
itcc-out2arch
"""""""""""""

* exit 1 when meet with invalid gaussian log file.
* support "-a" option

itcc-gjf2xyz
""""""""""""
* support send output to stdout

itcc-out2ene
""""""""""""

* still print the filename if does not find the ene.

itcc-xyz2gjf
""""""""""""
* support custom header

itcc-sumxyz
"""""""""""
* support read from stdin
* change output format


itcc-xyzpdb
"""""""""""

* output connect information


itcc-chiral
"""""""""""

* support more options

library
'''''''
* itcc/molecule/molecule
  - the bond contain H has a different maxbondlen
  - coords is assignable again
* itcc.molecule._rmsd add a new func: rmsd2

others
''''''

* Makefile: change default python from 'python2.4' to python

* python-setuptools
  * use the version scheme proposed by python-setuptools
  * rewrite setup.py with python-setuptools

0.8.1 and older versions
------------------------

itcc (0.8.1) unstable; urgency=low

  * separate itcc sub commands into sections.
  * add 'itcc chiral'.
  * add bash_completion support.

 -- LI Daobing <lidaobing@gmail.com>  Thu, 21 Dec 2006 11:24:24 +0800

itcc (0.8) unstable; urgency=low

  * itcc rmsd
    - support only one argument.
    - add options: '--atoms', '--atomsfile', '--atoms1', '--atoms1file',
    '--atoms2', '--atoms2file'.
  * 'itcc dmddat2dmddat' support new '-F' option.
  * add new function: 'itcc.Molecule.tools.logic_distance'.
  * new module: itcc.CCS2.triangle
    - new function: calc_ab
  * new module: itcc.CCS2.inner
    - new function: inner2xyz
  * module: itcc.CCS2.Mezei:
    - new function: r6_base
  * depends on higher version of python-scientific and python-scipy
  * swicth to cdbs+pycentral
  * itcc cmpxyztop support '-c' option

 -- LI Daobing <lidaobing@gmail.com>  Wed, 20 Dec 2006 09:45:09 +0800

itcc (0.7) unstable; urgency=low

  * add debian sub-directory.

 -- LI Daobing <lidaobing@gmail.com>  Fri, 24 Mar 2006 22:43:54 +0800

Version 0.6 - 2006-03-24

* itcc rmsd support mtxyz file as second argument.

Version 0.5 - 2006-03-17

* fix bug in 0.4
* new 'itcc dmddat2dmddat'

Version 0.4 - 2006-03-10

* new rotate.py
* new stats.py
* new `itcc shake'
* improve dmddat2mtxyz's speed.

Version 0.3 - 2006-02-21

* new `itcc xyz2pdb'
* remove license problem warning

Version 0.2.9 - 2006-02-21

* del xtc-related part from itcc

b9

* add license problem warning
* fix bug: itcc dmddat_fix

b8

* dynamic load libgmx.
* fix bug: write_xtc's box unit is nm.

b1-b7

* new 'itcc dmddat_fix', support both dmddat format.
* new 'itcc dmddat2mtxyz'
* fix bug: 'make dist' maybe miss new file(s).
* move src/ to itcc/ (it easy to write testsuite without install.)
* new 'itcc dmddat2xtc'
* itcc now is much faster at startup

Version 0.2.8

* add 'itcc scalexyz'
* add 'itcc columnmean'
* add 'itcc mtxyzstat'
* add 'itcc mol2top'
* add 'itcc onecolumn'
* [itcc.Tools.tools] add 'any', 'all'.
* add 'itcc removepbc'

Version 0.2.7

* use itcc to control all scripts
* add src/Tools/tor2freeene.py
* src/Molecule/_rmsd.cpp
   a better rmsd algorithm(consider transition and rotation)
* src/Torsionfit/getscandata.py
   rework   

Version 0.2.6

* add 'itcc printefit'

Version 0.2.4
   
* parmeval.py: rewrite, become a script
* Torsionfit: now the scandata.dat's third column is optional(default is 1.0)
* add README

Version 0.2.3

* fix a bug in readidx
* fix a bug in `make sdist'

Version 0.2.2

* A new version parmfit

Version 0.2.1

* merge torsionfit as itcc.Torsionfit and del duplicate module

Version 0.2

* Can do something version

Version 0.1	

* First can-run version.
