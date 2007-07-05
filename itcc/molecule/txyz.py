# $Id$

import numpy

def get_coords(ifile, idxs = None):
    line = ifile.readlines()
    if idxs is None:
        idxs = range(int(line.split()[0]))

    max_idx = max(idxs) + 1
    lines = []
    for i in range(max_idx):
        lines.append(ifile.readline())

    return numpy.array([[float(x) for x in lines[i].split()[2:5]] for i in idxs])
