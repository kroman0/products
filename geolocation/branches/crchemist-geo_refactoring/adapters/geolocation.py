from zope.interface import implements
from geo.interfaces import IPoint
from zope.app.annotation.interfaces import IAnnotations, IAnnotatable
from Products.CMFPlone.CatalogTool import registerIndexableAttribute
from persistent.mapping import  PersistentMapping

GEOLOCATION_KEY = "geolocation.adapters.geolocation"
class Point(object):
    implements(IPoint)

    def __init__(self, context):
        """ init  """
        self.annotations = IAnnotations(context)
        self.point = self.annotations.get(GEOLOCATION_KEY, None)
        if self.point == None:
            self.annotations[GEOLOCATION_KEY] = PersistentMapping()
            self.point = self.annotations[GEOLOCATION_KEY]
            self.point['targetId'] = ''
            self.point['extrude'] = 0
            self.point['tessellate'] = 0
            self.point['altitudeMode'] = 'clampToGround'
            self.point['coordinates']  = (0,0,0)

    def getCoordinates(self):
        return self.point['coordinates']

    def setCoordinates(self, coordinates):
        self.point['coordinates'] = coordinates

    def getAltitudeMode(self):
        return self.point['altitudeMode']

    def setAltitudeMode(self, altitudeMode):
        self.point['altitudeMode'] = altitudeMode

    def getTessellate(self):
        return self.point['tessellate']

    def setTessellate(self, tessellate):
        self.point['tessellate'] = tessellate

    def getExtrude(self):
        return self.point['extrude']

    def setExtrude(self, extrude):
        self.point['extrude'] = extrude

    def getTargetId(self):
        return self.point['targetId']

    def setTargetId(self, targetId):
        self.point['targetId'] = targetId

    coordinates = property(getCoordinates, setCoordinates, """ see interface """)
    altitudeMode = property(getAltitudeMode, setAltitudeMode, """ see interface """)
    tessellate = property(getTessellate, setTessellate, """ see interface """)
    extrude = property(getExtrude, setExtrude, """ see interface """)
    targetId = property(getTargetId, setTargetId, """ see interface """)

default = None
def geoLocation(obj, portal, **kw):
    """ return the location list """
    if hasattr(obj.aq_base, 'geoLocation'):
        return obj.geoLocation()
    adapter = IPoint(obj, None)
    if adapter:
        coord = adapter.coordinates[0:2]
        if not coord:
            return None
        else:
            return coord
    return default

registerIndexableAttribute('geoLocation', geoLocation)