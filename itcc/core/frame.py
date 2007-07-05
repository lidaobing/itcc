# $Id$

__revision__ = '$Rev$'

def parseframe(frame_str):
    if frame_str is None:
        return
    for range1 in frame_str.split(','):
        for range_ in range1.split():
            step = 1
            if '/' in range_:
                range_, step = tuple(range_.split('/'))
                step = int(step)
            if '-' in range_:
                begin, end = tuple([int(x) - 1 for x in range_.split('-')])
                end += 1
            else:
                begin = int(range_) - 1
                end = begin+1

            for x in range(begin, end, step):
                yield x
