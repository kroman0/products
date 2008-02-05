# zope 3 imports
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# Product imports
from geo.interfaces import IPoint
from Products.geolocation.interfaces.geolocation import IPointView

class PointView(BrowserView):

    implements(IPointView)

    def __init__(self, context, request):
        """ init view """
        self.context = context
        self.request = request
        self.location = IPoint(self.context, None)
        self.longitude = self.location and self.location.coordinates[0] or None
        self.latitude = self.location and self.location.coordinates[1] or None

    def editLocation(self, latitude=None, longitude=None):
        """ update location properties """
        self.location.coordinates = (longitude, latitude,0)
        self.context.reindexObject()

    def getLatitude(self):
       """ return point latitude """
       return self.latitude

    def getLongitude(self):
       """ return point longitude """
       return self.longitude