from zope.interface import Interface
from zope.interface import Attribute
from zope.schema import Float

class IGEOLocated(Interface):
    """GEO location cordinates
    """
    """
    longitude = Float(
        title=u"Longitude",
        description=u"",
        required = False )

    latitude = Float(
        title=u"Latitude",
        description=u"",
        required = False )
    """
    
    def getLongitude():
        """ return longtitude """

    def getLatitude():
        """ return latitude """
    
    def setLongitude(value):
        """ set longtitude """
    
    def setLatitude(value):
        """ set latitutde """

    def setLocation(latitude, longitude):
       """ set location  """

class IGEOLocatedView(Interface):
    """browser view
    """

    def editLocation(latitude, longitude):
        """ update location properties """

    def getLatitude():
        """ return geo latitude """

    def getLongitude():
        """ return geo longitude """