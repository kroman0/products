from zope.interface import Interface

class IMarkersListing(Interface):
    """ simple markers adapter that prepare markers listing for view
    """
   
    def listMarkers():
        """ return markers listing """

class IMarkersView(Interface):
    """  Markers view support interface
    """
    
    def listMarkers():
        """ return contained markers """
