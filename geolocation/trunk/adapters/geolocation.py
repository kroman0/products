from zope.interface import implements
from Products.geolocation.interfaces.geolocation import IGEOLocated
from zope.app.annotation.interfaces import IAnnotations, IAnnotatable
from Products.CMFPlone.CatalogTool import registerIndexableAttribute
from persistent.mapping import  PersistentMapping

GEOLOCATION_KEY = "geolocation.adapters.geolocation"

class GEOLocated(object):
    """ geolocation
    """
    implements(IGEOLocated)

    def __init__(self, context):
        """ init  """
        self.annotations = IAnnotations(context)
        self.geolocation = self.annotations.get(GEOLOCATION_KEY, None)
        if self.geolocation == None:
            self.annotations[GEOLOCATION_KEY] = PersistentMapping()
            self.geolocation = self.annotations[GEOLOCATION_KEY]
            self.geolocation['latitude']  = None
            self.geolocation['longitude'] = None

    def getLongitude(self): 
        """ return longtitude """
        return self.geolocation['longitude']

    def getLatitude(self):
        """ return latitude """
        return self.geolocation['latitude']

    def setLongitude(self, value):
        """ set longtitude """
        self.geolocation['longitude'] = float(value)

    def setLatitude(self, value):
        """ set latitutde """
        self.geolocation['latitude'] = float(value)

    def setLocation(self, latitude, longitude):
        """ set location """
        self.geolocation['longitude'] = float(longitude)
        self.geolocation['latitude'] = float(latitude)

default = None

def geoLocation(obj, portal, **kw):
    """ return the location list """
    if hasattr(obj.aq_base, 'geoLocation'):
        return obj.geoLocation()
    adapter = IGEOLocated(obj, None)
    if adapter:
        lng = adapter.getLongitude()
        lat = adapter.getLatitude()
        if not (lat or lng):
            return None
        else:
            return (lat, lng)
    return default
"""
def Longitude(obj, portal, **kw):
    adapter = IGEOLocated(obj, None)
    if adapter:
        return adapter.getLongitude()
    return default

def Latitude(obj, portal, **kw):
    adapter = IGEOLocated(obj, None)
    if adapter:
        return adapter.getLatitude()
    return default
"""
registerIndexableAttribute('geoLocation', geoLocation)
#registerIndexableAttribute('Longitude', Longitude)
#registerIndexableAttribute('Latitude', Latitude)
