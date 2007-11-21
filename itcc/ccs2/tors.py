import numpy
import bisect

criterion = 1

class TorsSet:
    def __init__(self, data=None):
        self._data = []
        if data is None:
            data = []
        for item in data:
            self.append(item)
        
    def append(self, item):
        bisect.insort(self._data, item)
        
    def __contains__(self, item):
        if not self._data:
            return False
        for newitem in self.vary(item):
            if self._contain(newitem):
                return True
        return False

    def _contain(self, item):
        size = len(self._data)
        pos = bisect.bisect(self._data, item)
        idx = pos - 1
        while idx >= 0:
            if item[0] - self._data[idx][0] > criterion:
                break
            if self.isnear(self._data[idx], item):
                return True
            idx -= 1

        idx = pos    
        while idx < size:
            data = self._data[idx]
            if data[0] - item[0] > criterion:
                break
            if self.isnear(data, item):
                return True
            idx += 1
        return False

    def vary(item):
        doubledata = item * 2
        minusdoubledata = tuple([-x for x in doubledata])
        size = len(item)
        for i in range(size):
            yield doubledata[i:i+size]
            yield doubledata[i+size:i:-1]
            yield minusdoubledata[i:i+size]
            yield minusdoubledata[i+size:i:-1]
    vary = staticmethod(vary)

    def isnear(item1, item2):
        for x1, x2 in zip(item1, item2):
            abso = abs(x1-x2)
            if criterion < abso < 360 - criterion:
                return False
        return True
    isnear = staticmethod(isnear)

    def distance(item1, item2):
        return max([abs(x1-x2) for x1, x2 in zip(item1, item2)])
    distance = staticmethod(distance)
    

class Tors(object):
    __slots__ = ['_data', '_sortdata']

    def __init__(self, data):
        self._data = numpy.array(data)
        self._sortdata = [abs(x) for x in data]
        self._sortdata.sort()
        self._sortdata.insert(0, -self._sortdata[0])
        self._sortdata.append(360 - self._sortdata[-1])

    def __eq__(self, other):
        n = len(self._data)
        odata = other._data
        doubledata = numpy.array(list(self._data) * 2)
        criter = criterion

        for x in odata:
            x = abs(x)
            idx = bisect.bisect(self._sortdata, x)
            if self._sortdata[idx-1] + criter < x < self._sortdata[idx] - criter:
                return False
        
        for i in range(n):
            if max(abs(doubledata[i:i+n] - odata)) < criter or \
               max(abs(doubledata[i:i+n] + odata)) < criter or \
               max(abs(doubledata[i+n:i:-1] - odata)) < criter or \
               max(abs(doubledata[i+n:i:-1] + odata)) < criter:
                return True
        return False

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return `self._data`


if __name__ == '__main__':
    a = Tors([1.1, 2.2, 3.3])
    b = Tors([3.2, 2.3, 1.1])
    c = Tors([1.1, 2.1, 2.1])
    print a, b, c
    print a == b
    print a == c
    print b == c
    print a in [b, c]
        
            
