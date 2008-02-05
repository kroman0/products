from zope.interface import implements
from Products.geolocation.interfaces.geomap import IGEOMap
from zope.app.annotation.interfaces import IAnnotations, IAnnotatable
from persistent.mapping import  PersistentMapping

GEOMAP_KEY = "geolocation.adapters.geomap"

class GEOMap(object):
    """ geomap
    """
    implements(IGEOMap)

    def __init__(self, context):
        """ init  """
        self.annotations = IAnnotations(context)
        self.geomap = self.annotations.get(GEOMAP_KEY, None)
        if self.geomap == None:
            self.annotations[GEOMAP_KEY] = PersistentMapping()
            self.geomap = self.annotations[GEOMAP_KEY]
            self.geomap['mapcenter'] = None
            self.geomap['mapzoom']   = None
            self.geomap['maptype']   = None

    def getMapCenter(self):
        """ return map center """
        return self.geomap['mapcenter']

    def getMapZoom(self):
        """ return map zoom """
        return self.geomap['mapzoom']

    def getMapType(self):
        """ return map type """
        return self.geomap['maptype']


    def setMap(self, mapcenter, mapzoom, maptype):
        """ set map options """
        self.geomap['mapcenter'] = mapcenter
        self.geomap['mapzoom'] = mapzoom
        self.geomap['maptype'] = maptype
