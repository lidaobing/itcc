# $Id$

class MezeiBase(object):
     
    
    def R6(self, coords, atmidx, dismat, shakedata):
        '''Wrapped R6 algorithm, include R6 and shakeH'''
        shakes = [shakedata[idx] for idx in atmidx[1:-1]]
        for baseresult in self.__R6(coords, atmidx, dismat):
            newcoords = coords.copy()
            abs_dist = 0.0 
            for idx, newcoord in baseresult.items():
                newcoords[idx] = newcoord
                abs_dist += sum(abs(newcoord - coords[idx]))
            if abs_dist < self.min_abs_dist:
                continue
            for refidxs, sidechain_ in shakes:
                baseresult.update(sidechain.movesidechain(coords, newcoords, refidxs, sidechain_))
            yield baseresult
