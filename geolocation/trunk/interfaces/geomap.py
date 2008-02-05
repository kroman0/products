from zope.interface import Interface

class IGEOMap(Interface):
    """GEO Map options
    """

    def getMapCenter():
        """ return map center """

    def getMapZoom():
        """ return map zoom """

    def getMapType():
        """ return map type """

    def setMap(mapcenter, mapzoom, maptype):
       """ set map options  """

class IGEOMapView(Interface):
    """browser view
    """

    def editMapOptions(mapcenter, mapzoom, maptype):
        """ update map options """

    def getMapCenter():
        """ return map center """

    def getMapZoom():
        """ return map zoom """

    def getMapType():
        """ return map type """