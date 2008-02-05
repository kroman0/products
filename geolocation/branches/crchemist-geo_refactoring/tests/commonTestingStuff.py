from zope.interface.verify import verifyClass
from Testing.ZopeTestCase.PortalTestCase import user_name, user_password

from Products.CMFCore.utils import getToolByName

from geo.interfaces import IPoint
from Products.geolocation.interfaces.geolocation import IPointView
from Products.geolocation.interfaces.geomap import IGEOMap, IGEOMapView
from Products.geolocation.adapters.geolocation import Point
from Products.geolocation.adapters.geomap import GEOMap
from Products.geolocation.browser.location import PointView
from Products.geolocation.browser.map import GEOMapView

from Products.PloneTestCase import PloneTestCase

PRODUCTS=('geolocation',)

map(PloneTestCase.installProduct, PRODUCTS)
PloneTestCase.setupPloneSite(products=PRODUCTS)

PRODUCT = 'geolocation'

def maps_login(self, role):
    """  Utility method for login under required role """
    from Testing.ZopeTestCase.PortalTestCase import user_name, user_password
    if role == 'manager':
        self.loginAsPortalOwner()
    elif role == 'member':
        self.login(user_name)
    elif role == 'another_member':
        self.login('another_member')
    elif role == 'anonym':
        self.logout()

# Installation testing stuff
PORTAL_TYPES = ['Document', 'News Item', 'Event', 'Link', 'Image']
GEO_INDEX = 'geoLocation'
LATITUDE = 2.3
LONGITUDE = 3.2
ALTITUDE = 2.1
MAP_CENTER = (9,9)
MAP_ZOOM = 6
MAP_TYPE = 'hybrid'
