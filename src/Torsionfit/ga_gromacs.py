# $Id$
# -*- coding: utf8 -*-
#遗传算法
#copyleft by nichloas@sohu.com

from random import shuffle

__revision__ = '$Rev$'

class Chromosome:
    '''
    变量：
    data:     float(n x 1)
    mark:     float    (less is better)
    '''

    def __init__(self):
        self.data = []
        self.mark = 0

    def __cmp__(self, chromo):
        return cmp(self.mark, chromo.mark)

    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, item):
        self.data[key] = item

    def __len__(self):
        return len(self.data)


class GA:
    '''
    Genetic Algorithm

    变量：
    self.n:           integer, number of chromosomes
    self.len:         integer, len of chromosome
    self.chromosomes: Chromosome(self.n * 1), chromosomes
    self.limit:       float(self.len * 2), limit of genes

    self.cycle:       integer, count of cycle
    self.maxcycle:    integer
    self.goodcycle:   integer
    self.maxgoodcycle:integer

    self.P_select:    float, 每轮淘汰率
    self.P_mutation:  float, 每轮变异率

    self.feval:       function, 评价函数

    方法：
    readlimit(ifname):    read self.limit from file
    init()

    Usage:
    ga = GA()
    ga.readlimit(ifname)
    ga.n = ...
    ga.feval = ...
    ga.maxcycle = ...
    ga.maxgoodcycle = ...
    ga.mainloop()
    
    
    
    
    
    
    '''
    def __init__(self, limitfname, n, feval):
        self.readlimit(limitfname)

        self.n = n
        self.chromosomes = []
        self.mkchrom(n)

        self.feval = feval
        
        self.P_select = 0.2
        self.P_mutation = 0.1
        self.maxcycle = 250
        self.maxgoodcycle = 50
        
        self.cycle = 0
        self.goodcycle = 0

    def readlimit(ifname):
        """
        参数文件格式为： '%f %f\n'
        """
        try:
            ifile = file(ifname)
            lines = ifile.readlines()
            ifile.close()
        except IOError:
            print "Can't open file: %s" % ifname
            raise

        words = [x.split() for x in lines]

        try:
            self.limit = [[float(y) for y in x] for x in words]
            if len(filter(lambda x: len(x) != 2, self.limit)):
                raise ValueError
        except ValueError:
            print 'limit file format error'
            raise

    def mkchrom(self, n):
        if isinstance(n, int) or n < 1:
            print 'n should be a positive integer'
            raise ValueError
        for i in range(n):
            chromo = Chromosome()
            chromo.data = [random.uniform(x[0], x[1]) for x in self.limit]
            self.chromosomes.append(chromo)

    def mainloop(self):
        for i in range(maxcycle):
            self.eval()
            self.select()
            
            
        

    def eval(self):
        for x in self.chromosomes:
            x.mark = self.feval(x.data)
        
    def select(self):
        self.chromosomes.sort()
        self.keep = int(n * (1-self.P_select))

        self.chromosomes = self.chromosomes[:keep]
        shuffle(self.chromosomes)
        
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

