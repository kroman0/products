from zope.interface import Interface

class IDomainsMapExtractor(Interface):

    def getDomainsMap():
        """ Return sorted by sybpath length tupple
            of (subpath, domain name) tuple.
        """
    def setDomainsMap():
        """ Set tupple of (subpath, domain name) tuples
        """
