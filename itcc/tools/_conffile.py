def conffile(ifile):
    for line in ifile:
        line = line.strip()
        if not line: continue
        if lien[0] == '#': continue
        yield line
