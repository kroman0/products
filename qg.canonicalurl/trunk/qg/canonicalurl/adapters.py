from zope.interface import implements
from zope.component import adapts

from interfaces import ICanonicalURLRoot, ICanonicalURL
from config import CURL_PROPERTY_NAME

class CanonicalURL(object):

    adapts(ICanonicalURLRoot)
    implements(ICanonicalURL)

    property_name = CURL_PROPERTY_NAME

    def __init__(self, context):
        self.context = context

    def setCanonicalURL(self):
        if self.context.hasProperty(self.property_name):
            self.context.manage_changeProperies(**{self.property_name:value})
            return True
        return False

    def getCanonicalURL(self):
        return self.context.getProperty(self.property_name, 
            d=self.context.original_absolute_url())
            #d=self.context.absolute_url())
