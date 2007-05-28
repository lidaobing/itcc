# $Id$

__version__ = '$Rev$'[6:-2]

import xml.sax
import xml.sax.handler

class MassHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.ready = False
        self.atomicNumber_ready = False
        self.mass_ready = False
        self.res = {}
    def startElement(self, name, attrs):
        if name == 'atom':
            self.ready = True
        if self.ready \
                and name == 'scalar' \
                and 'dictRef' in attrs.getNames():
                    if attrs.getValue('dictRef') == "bo:atomicNumber":
                        self.atomicNumber_ready = True
                    elif attrs.getValue('dictRef') == 'bo:mass':
                        self.mass_ready = True

    def endElement(self, name):
        if name == 'atom':
            self.ready = False

    def characters(self, content):
        if self.atomicNumber_ready:
            self.atomicNumber = int(content)
            self.atomicNumber_ready = False
        if self.mass_ready:
            self.res[self.atomicNumber] = float(content)
            self.mass_ready = False

def load_mass():
    res = MassHandler()
    xml.sax.parse('/usr/share/bodr/elements.xml', res)
    return res.res

if __name__ == '__main__':
    print '# generated by itcc.bodr._load_mass %s' % __version__
    print 'mass = ',
    import pprint
    pprint.pprint(load_mass())
