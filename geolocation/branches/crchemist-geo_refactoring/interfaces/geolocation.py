from zope.interface import Interface
from zope.interface import Attribute
from zope.schema import Float

class IPointView(Interface):
    """browser view
    """

    def editLocation(latitude, longitude):
        """ update location properties """

    def getLatitude():
        """ return point latitude """

    def getLongitude():
        """ return point longitude """