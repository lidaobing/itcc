
def genR(conns):
    result = []
    for i in range(len(conns)):
        for x in conns[i]:
            if i+1 < x:
                result.append([i,x-1])
    return result

def genA(conns):
    result = []
    for i in range(len(conns)):
        for j in range(len(conns[i])):
            for k in range(j+1,len(conns[i])):
                result.append([conns[i][j]-1, i, conns[i][k]-1])
    return result

def genD(conns):
    result = []
    Rs = genR(conns)
    for x in Rs:
        if len(conns[x[0]]) == 1 or len(conns[x[1]]) == 1:
            continue
        for y in conns[x[0]]:
            if y-1 == x[1]:
                continue
            for z in conns[x[1]]:
                if z-1 == x[0] or y == z:
                    continue
                result.append([y-1, x[0], x[1], z-1])
    return result
