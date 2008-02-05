from zope.interface import implements
from Products.qPloneGoogleMaps.interfaces.markers import IMarkersListing

class MarkersListing(object):
    """ simple markers adapter that prepare markers listing for view
    """
    implements(IMarkersListing)
    
    def __init__(self, context):
        """ init  """
        self.context = context
    
    def listMarkers(self):
        """ return markers listing """
        if self.context.portal_type == "Topic":
            contentsMethod = self.context.queryCatalog
        elif self.context.portal_type in ["Folder", "Large Plone Folder"]:
            contentsMethod = self.context.getFolderContents
        else:
             return None
        markers = [marker for marker in contentsMethod() if marker.geoLocation]
        return markers
