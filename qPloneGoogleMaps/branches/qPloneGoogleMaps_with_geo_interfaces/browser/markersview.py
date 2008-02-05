# zope 3 imports
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# Product imports
from Products.qPloneGoogleMaps.interfaces.markers import IMarkersView
from Products.qPloneGoogleMaps.adapters.markers import IMarkersListing

class MarkersView(BrowserView):

    implements(IMarkersView)
          
    def __init__(self, context, request):
        """ init view """
        self.context = context
        self.request = request
        adapter = IMarkersListing(self.context, None)
        if adapter:
            self.markers = adapter.listMarkers()
        else:
            self.markers = None

    def listMarkers(self):
        """ return contained markers """
        return self.markers