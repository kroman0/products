from zope.interface import Interface

class ICanonicalURLRoot(Interface):
    """Marker interface for canonical URL provider
    """

class ICanonicalURL(Interface):
    """Get/Set Canonical URL property value
    """
    def getCanonicalURL():
        """Return canonical URL:
           calculated from 'canonical_url' property
           on ICanonicalURL marked object and relative
           path from it OR absolute_url otherwise.
        """

    def setCanonicalURL():
        """Set canonical URL
        """
