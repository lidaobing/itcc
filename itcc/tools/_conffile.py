def conffile(ifile):
    for line in ifile:
        line = line.strip()
        if not line or line[0] == '#':
            continue
        yield line
