import re
from molecular import Molecular, Atom

def beginoflink(ifile, linknum):
    restr = '(Enter .*l%d.exe)' % linknum
    prog = re.compile(restr)

    while True:
        line = ifile.readline()
        if line == '':
            return False
        elif prog.search(line):
            return True
    return None

def getxyz_202(ifile):
    mol = Molecular()

    while 1:
        line = ifile.readline()
        if line.find('Input orientation:') != -1:
            break

    ifile.readline()
    ifile.readline()
    ifile.readline()
    ifile.readline()

    while 1:
        line = ifile.readline()
        words = line.split()
        if len(words) != 6:
            break
        atom = Atom()
        atom.no = int(words[1])
        atom.coords = [float(x) for x in words[3:6]]
        mol.atoms.append(atom)

    return mol

def checkoptimized(ifile):
    while 1:
        line = ifile.readline()
        if line == '':
            return False
        if line.find('Leave Link') != -1:
            return False
        if line.find('Optimized Parameters') != -1:
            return True
    return None
        
def getscandata(ifname):
    result = []

    ifile = file(ifname)

    while True:
        if beginoflink(ifile, 202):
            mol = getxyz_202(ifile)
        else:
            break

        if beginoflink(ifile, 103):
            if checkoptimized(ifile):
                result.append(mol)
        else:
            break
    
    ifile.close()
    return result

if __name__ == '__main__':
    import sys
    from itcc.Molecule import write
    if len(sys.argv) == 3:
        mols = getscandata(sys.argv[1])
        for i in range(len(mols)):
            ofilename = sys.argv[2] + '%02d.xyz' % (i+1)
            write.writexyz(mols[i], ofilename)
    else:
        print 'Usage: %s ifilename ofileprefix' % sys.argv[0]
        
        
