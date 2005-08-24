# -*- coding: utf-8 -*-
# $Id$
#遗传算法

import random

class GA:
    "Genetic Algorithm"
    def __init__(self):
        self.chromosomes = []
        self.limit = []
        self.cycle = 0
        self.P_select = 0.2
        self.P_mutation = 0.1
        self.feval = None
        self.maxcycle = 250
        self.maxgoodcycle = 50
        pass

    def init(self):
        self.n = len(self.chromosomes)
        self.keep = int(self.n * (1 - self.P_select))
        self.length = len(self.chromosomes[0])

    def mainloop(self):
        self.init()
        for i in range(maxcycle):
            pass



    def eval(self):
        self.mark = [self.feval(x) for x in self.chromosomes]

    def select(self):
        n = len(self.chromosomes)
        keep = int(n * (1-self.P_select))

        markb = self.mark[:]
        markb.sort()
        threshold = markb[keep]

        result = []
        for i in range(n):
            if self.mark[i] < threshold:
                result.append(self.chromosomes[i])
        self.chromosomes = result

    def mutation(self):
        for i in range(len(self.chromosomes)):
            for j in range(len(self.chromosomes[i])):
                if random.random() < self.P_mutation :
                    self.chromosomes[i][j] = random.uniform(self.limit[j][0], self.limit[j][1])

    def crossover(self):
        n = len(self.chromosomes)
        length = len(self.chromosomes[0])
        l = range(n)
        random.shuffle(l)

        for i in range(0,n,2):
            a = l[i]
            b = l[i+1]
            point = random.randint(1,length-1)
            temp = self.chromosomes[a][:point] + self.chromosomes[b][point:]
            self.chromosomes[b] = self.chromosomes[b][:point] + self.chromosomes[a][point:]
            self.chromosomes[a] = temp

    def newrandom(self):
        n = self.n - self.keep
        for i in range(n):
            self.chromosomes.append([random.uniform(x[0], x[1]) for x in self.limit])

if __name__ == '__main__':
    ga = GA()
    ga.chromosomes = [[random.randint(0,9) for x in range(10)] for x in range(10)]
    ga.limit = ((0,9),) * 10
    ga.feval = lambda x: reduce(lambda x,y: x+y*y, x, 0)

    print '\n'.join([str(x) for x in ga.chromosomes]) + '\n'

    ga.eval()
    ga.select()
    print '\n'.join([str(x) for x in ga.chromosomes]) + '\n'

    ga.mutation()
    print '\n'.join([str(x) for x in ga.chromosomes]) + '\n'

    ga.crossover()
    print '\n'.join([str(x) for x in ga.chromosomes]) + '\n'

