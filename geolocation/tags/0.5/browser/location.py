# zope 3 imports
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# Product imports
from Products.geolocation.interfaces.geolocation import IGEOLocated, IGEOLocatedView

class GEOLocatedView(BrowserView):

    implements(IGEOLocatedView)

    def __init__(self, context, request):
        """ init view """
        self.context = context
        self.request = request
        self.location = IGEOLocated(self.context, None)
        self.latitude = self.location and self.location.getLatitude() or None
        self.longitude = self.location and self.location.getLongitude() or None

    def editLocation(self, latitude=None, longitude=None):
        """ update location properties """
        self.location.setLocation(latitude, longitude)
        self.context.reindexObject()

    def getLatitude(self):
       """ return location latitude """
       return self.latitude

    def getLongitude(self):
       """ return location longitude """
       return self.longitude