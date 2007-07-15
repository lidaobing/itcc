ITCC
====

itcc is a set of scripts used in my works.

.. contents::

Author and Copyright Holders
-----------------------------

LI Daobing
  <lidaobing at gmail dot com>

WU Yundong
  http://home.ust.hk/%7Echydwu/

Peking University
  http://www.pku.edu.cn/

Install
-------

1. Install python_, python-numpy_, lapack3_, easy_install_ on your computer. On
   a Debian_ system, you only need install following packages, ``python``,
   ``python-numpy``, ``lapack3`` or ``atlas3-base``, ``python-setuptools``.

.. _python: http://www.python.org
.. _python-numpy: http://www.numpy.org
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _lapack3: http://en.wikipedia.org/wiki/LAPACK
.. _Debian: http://www.debian.org

2. run following command as root: ``easy_install itcc``, now I only upload a
   python2.4-i386 version to pypi, if you need other version, mail me.


Programs
--------

Common rules:

* If you call a script without arguments, it will print a brief usage.
* If a script accept a filename as input or output, often it will support/treat "-" as the stand input or standard output.
* If you find ``fname...`` in the brief usage, it means that it support more than one fname in arguments.

OK, if you find any bug in these scripts or this documention, don't hesitate to
tell me, you can find my email address in the top of this page.

General
~~~~~~~

itcc
''''

print version information of this package.

File Format Convert
~~~~~~~~~~~~~~~~~~~

openbabel_ provide many file format converter, but not all.

.. _openbabel: http://openbabel.sourceforge.net

itcc-gjf2xyz, itcc-xyz2gjf, itcc-xyz2gro, itcc-xyz2pdb
''''''''''''''''''''''''''''''''''''''''''''''''''''''

provide molecule converter between these formats, maybe you can found the
format specifcation on the openbabel's homepage.

* gjf: Gaussian input format, does not support internal coordinate.
* xyz: TINKER xyz format.
* gro: GROMACS gro format.
* pdb: Protein Data Bank format.  

``itcc-xyz2gjf`` support ``-h`` option to specify a customized header file, I
use this script to generate a bundle of gjf input file.

Gaussian Related Programs
~~~~~~~~~~~~~~~~~~~~~~~~~

These is another gaussian related program called hirshfeld_, written in C++,
released under GPL, which can calculte hirshfeld charge from fchk file, as
rubbish as this package.

.. _hirshfeld: http://code.google.com/p/hirshfled

itcc-out2arch
'''''''''''''

Pick the arch information in the end of the gaussian log file and convert it to
a human readable format. Default it will only print the coordinate part, which
is ready as an input for the next step's calculation. With ``-a`` option, it
will print all information.

itcc-out2ene
''''''''''''

Pick the energy from gaussian log file, support multi file name in argument.

Tinker XYZ Format
~~~~~~~~~~~~~~~~~

itcc-rotate-to
''''''''''''''

Rotate molecule to make the given atoms as closer as possible to given
coordinate (minimal rmsd on given atoms).

Sometimes I generate some random molecules, then minimize to fulfill given
constrainis. Without this script, this molecule is highly distorted when
minimization, the chiral info, or double bound is broken in minimization. I
use this script to preprocess the molecule, then the minimization is much
smooth than previous.

itcc-

Undocumented Programs
~~~~~~~~~~~~~~~~~~~~~

I am lazy. So following commands is not documented.

- itcc
- itcc-makecyclicalkane
- itcc-stats
- itcc-calcangle
- itcc-ene2agr
- itcc-enestep2countstep
- itcc-random-protein-input
- itcc-loopverify
- itcc-count
- itcc-mirrormol
- itcc-printbonds
- itcc-detailcmp
- itcc-rg
- itcc-pyramid-check
- itcc-loopdetect
- itcc-out2ene
- itcc-out2arch
- itcc-optimizes
- itcc-chiral
- itcc-confsearch
- itcc-catordiff
- itcc-detectloop
- itcc-dmddummy
- itcc-scalexyz
- itcc-columnmean
- itcc-almostequaldiff
- itcc-shake
- itcc-mtxyzstat
- itcc-mol2top
- itcc-mtxyzrg
- itcc-sumxyz
- itcc-parmeval
- itcc-dmddat_fix
- itcc-onecolumn
- itcc-settype
- itcc-sumparam
- itcc-removepbc
- itcc-dmddat2dmddat
- itcc-parmfit
- itcc-cmpxyztop
- itcc-simpparam
- itcc-tor2freeene
- itcc-rmsd
- itcc-rmsd2
- itcc-dmddat2mtxyz
- itcc-printefit
- itcc-constrain
- itcc-loop2looptor
- itcc-idx-verify
- itcc-molcenter
- itcc-rotate-to
- itcc-histogram
- itcc-tordiff
- itcc-moldiff

THANKS
------

SHA Yao
  shayao_pku at yahoo dot com dot cn

ZUO Chunshan
  chunshan at gmail dot com

More
----

* If you need a binary package for other platform, mail me. And I will not
  backport it to python2.2.
* If you need source code, mail me.
* If you find bug in this package, mail me.
* If you need a feature, mail me.
* If you find that this package is a rubbish, yell it in  your room, don't mail me.
* If you have extra money, beer, manga books, mail me.
