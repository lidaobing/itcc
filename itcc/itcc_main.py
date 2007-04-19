# $Id$

__revision__ = '$Rev$'

import sys
import os.path
import itcc

subscript = [
    ('Gaussian', {
        'out2arch':   ('tools.out2arch', 'gaussian out to arch file'),
        'out2ene':    ('tools.out2ene', 'gaussian out to ene')
    }),
    ('Tinker', {
        'gjf2xyz':    ('molecule.gjf2xyz', 'convert gjf to xyz'),
        'xyz2gjf':    ('tools.xyz2gjf', 'xyz to gjf format'),
        'xyz2gro':    ('tools.xyz2gro', 'xyz to gro format'),
        'xyz2pdb':    ('molecule.xyz2pdb', 'xyz to pdb format'),
        'optimizes':  ('tinker.optimizes', 'optimizes a series of xyz files(broken)'),
    }),
    ('Molecule', {
        'chiral': ('molecule.chiral', 'calculate chirality'),
        }),
    ('CCS2', {
        'detectloop': ('ccs2.detectloop', 'detect loop'),
        'catordiff':  ('ccs2.catordiff', 'cyclic alkane torsion diffrent'),
        'confsearch': ('ccs2.confsearch', 'conformational search'),
        }),
    ('Other', {
        'almostequaldiff': ('tools.almostequaldiff', 'almost equal diff'),
        'cmpxyztop':  ('molecule.cmpxyztop', 'compare topology of two xyz files'),
        'columnmean': ('tools.columnmean', 'mean for column'),
        'constrain':  ('tinker.constrain', 'generate a constrain tinker.key'),
        'dmddummy':   ('tools.dmddummy', 'dmddummy'),
        'dmddat2mtxyz':('molecule.dmddat2mtxyz', 'convert dmddat file to mtxyz'),
        'dmddat2dmddat':('tools.dmddat2dmddat', 'convert dmddat file to dmddat'),
        'mol2top':    ('molecule.mol2top', 'mol to top'),
        'mtxyzrg':    ('tools.mtxyzrg', 'multi tinker xyz file\'s rg'),
        'mtxyzstat':  ('tools.mtxyzstat', 'multi tinker xyz stat'),
        'onecolumn':  ('tools.onecolumn', 'change multi columns file to one colum'),
        'dmddat_fix': ('tools.dmddat_fix', 'fix olddmddat file'),
        'parmeval':   ('torsionfit.parmeval', 'evaluate parameter files'),
        'parmfit':    ('torsionfit.parmfit', 'parm fit'),
        'printefit':  ('torsionfit.printefit', 'print efit'),
        'removepbc':  ('molecule.removepbc', 'remove pbc'),
        'rmsd':       ('molecule.rmsd', 'rmsd'),
        'scalexyz':   ('tools.scalexyz', 'scale xyz'),
        'settype':    ('molecule.settype', 'change the types of xyz file'),
        'shake':      ('tools.shake', 'shake molecule'),
        'simpparam':  ('tinker.simpparam', 'simplify parameter'),
        'sumxyz':     ('tools.sumxyz', 'summary xyz file\'s info'),
        'sumparam':   ('tools.sumparam', 'choose params from tinker parameter file'),
        'tor2freeene':('tools.tor2freeene', 'torsion to free energy'),
    })
    ]

def help():
    basename = os.path.basename(sys.argv[0])

    print 'Version:', itcc.__version__
    print
    print 'Sub-commands:'
    for section_key, section in subscript:
        print ' ' + section_key
        for k, v in sorted(section.iteritems()):
            print '  %s %-12s  %s' % (basename, k, v[1])
        print
    print 'report bugs to <lidaobing@gmail.com>'

def main():
    if len(sys.argv) == 1:
        help()
        sys.exit(0)

    key = sys.argv[1]
    subcmd_dict = {}
    for _, section in subscript:
        subcmd_dict.update(section)

    if key == '--version':
        print 'itcc', itcc.__version__
    elif key in ['-h', '--help', 'help']:
        help()
    elif key in subcmd_dict:
        del sys.argv[0]
        mod_name = 'itcc.' + subcmd_dict[key][0]
        __import__(mod_name)
        sys.modules[mod_name].main()
    else:
        sys.stderr.write('Unknown option: %s\n' % key)
        sys.stderr.write("Type 'itcc help' for usage.\n")
        sys.exit(1)

if __name__ == '__main__':
    main()