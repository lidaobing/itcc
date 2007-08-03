ITCC
====

.. contents::

Hello, I am LI Daobing, itcc is a set of scripts used in my works.

Author and Copyright Holders
-----------------------------

LI Daobing
  lidaobing@gmail.com

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
   python2.4-i386 version to pypi, and it should be installable from python2.3
   to python 2.5, and also can be used in other platform. If you need other
   version, mail me.

Programs
--------

Common rules:

* If you call a script without arguments, it will print a brief usage.
* If a script accept a filename as input or output, often it will support/treat
  "-" as the stand input or standard output.
* If you find ``fname...`` in the brief usage, it means that it support more
  than one fname in arguments.

OK, if you find any bug in these scripts or this documention, don't hesitate to
tell me, you can find my email address in the top of this page.

General
~~~~~~~

itcc
''''

print version information of this package.

Conformational Search
~~~~~~~~~~~~~~~~~~~~~

itcc-confsearch
'''''''''''''''

A new conformational search based on exactly loop closure. Support cyclic
and acyclic alkane, cyclic and acylic peptide, loop region.

I know this description will confuse you. Then just run following scripts to
got all 261 conformations of cycloheptadecane in 3.0 kcal/mol in MM2 force
field. (install tinker first)

::

  itcc-makecyclicalkane 17 > 1.xyz
  minimize 1.xyz /usr/share/tinker/params/mm3.prm 0.01
  cp 1.xyz_2 a.xyz
  cp /usr/share/tinker/params/mm2.prm .
  itcc-confsearch -f mm2 -s 3 -k 3 a.xyz > test1.log
  
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

itcc-makecyclicalkane
'''''''''''''''''''''

Make a cyclic alkane in txyz format and MM2/MM3 force field. Coordinate is
pertubated to make it not on a saddle point. I suggest you use MM3 force field
to minimize this structure to avoid get a pyramid conformation (all four single
bond of a carbon is in one side).

itcc-random-protein-input
'''''''''''''''''''''''''

Randomize the phi and psi angle from a TINKER protein's input file.

itcc-scalexyz
'''''''''''''

scale all coords of a TINKER xyz file. I have forgotten why I write this.

Data Processing
~~~~~~~~~~~~~~~

itcc-count
''''''''''

Print every unique word from the input file and the word's appearance times.

itcc-stats
''''''''''

Print the sum, min, max, median, mean, std of the data from the input file.

Others
~~~~~~

itcc-calcangle
''''''''''''''
given the lengths or a triangle, output the angles in degree. (maybe I should
remove this script)

Undocumented Programs
~~~~~~~~~~~~~~~~~~~~~

I am lazy. So following commands is not documented.

- itcc-almostequaldiff
- itcc-catordiff
- itcc-chiral
- itcc-cmpxyztop
- itcc-columnmean
- itcc-constrain
- itcc-detailcmp
- itcc-detectloop
- itcc-dmddat2dmddat
- itcc-dmddat2mtxyz
- itcc-dmddat_fix
- itcc-dmddummy
- itcc-ene2agr
- itcc-enestep2countstep
- itcc-histogram
- itcc-idx-verify
- itcc-loop2looptor
- itcc-loopdetect
- itcc-loopverify
- itcc-mirrormol
- itcc-mol2top
- itcc-molcenter
- itcc-moldiff
- itcc-mtxyzrg
- itcc-mtxyzstat
- itcc-onecolumn
- itcc-optimizes
- itcc-out2arch
- itcc-out2ene
- itcc-parmeval
- itcc-parmfit
- itcc-pdbqchargesum
- itcc-printbonds
- itcc-printefit
- itcc-pyramid-check
- itcc-relative
- itcc-removepbc
- itcc-rg
- itcc-rmsd
- itcc-rmsd2
- itcc-rotate-to
- itcc-settype
- itcc-shake
- itcc-simpparam
- itcc-sumparam
- itcc-sumxyz
- itcc-tor2freeene
- itcc-tordiff

THANKS
------

SHA Yao
  shayao_pku at yahoo dot com dot cn

ZUO Chunshan
  chunshan at gmail dot com

NEWS
----

In a spearate page news.xhtml_.

.. _news.xhtml: news.xhtml

More
----

* If you need a binary package for other platform, mail me. And I will not
  backport it to python2.2.
* If you need source code, mail me.
* If you find bug in this package, mail me.
* If you need a feature, mail me.
* If you find that this package is a rubbish, yell it in  your room, don't mail me.
* If you have extra money, beer, manga books, mail me.
