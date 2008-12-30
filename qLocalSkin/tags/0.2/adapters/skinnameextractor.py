from zope.component import adapts
from zope.interface import implements

from Products.qLocalSkin.interfaces import IShiftPortalUrl
from interfaces import ISkinNameExtractor
from Products.qLocalSkin.config import PROPERTY_NAME

class SkinNameExtractor(object):
    """ Extract skin name from context's properties. """

    implements(ISkinNameExtractor)
    adapts(IShiftPortalUrl)

    property_name = PROPERTY_NAME

    def __init__(self, context):
        self.context = context

    def getSkinName(self):
        skin_name = self.context.getProperty(self.property_name, d=None)
        return skin_name

    def setSkinName(self, value):
        if self.context.hasProperty(self.property_name):
            self.context.manage_changeProperies(**{self.property_name:value})
            return True
        return False
