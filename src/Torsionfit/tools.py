# $Id$
'''Common parts for parmeval and parmfit'''

__revision__ = '$Rev$'

def readdat(datfname):
    fnames = []
    enes = []
    weights = []
    for line in file(datfname):
        words = line.split()
        assert len(words) in [2, 3]
        fnames.append(words[0])
        enes.append(float(words[1]))
        if len(words) == 2:
            weights.append(1.0)
        else:
            weights.append(float(words[2]))
    return (fnames, enes, weights)


