# zope 3 imports
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# Product imports
from Products.geolocation.interfaces.geomap import IGEOMap, IGEOMapView

class GEOMapView(BrowserView):

    implements(IGEOMapView)

    def __init__(self, context, request):
        """ init view """
        self.context = context
        self.request = request
        self.map = IGEOMap(self.context, None)

    def editMapOptions(self, mapcenter, mapzoom, maptype):
        """ update map options """
        self.map.setMap(mapcenter, mapzoom, maptype)
        self.context.reindexObject()

    def getMapCenter(self):
        """ return map center """
        return self.map.getMapCenter()

    def getMapZoom(self):
        """ return map zoom """
        return self.map.getMapZoom()

    def getMapType(self):
        """ return map type """
        return self.map.getMapType()
