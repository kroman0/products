from zope.interface import Interface, Attribute

class ISkinNameExtractor(Interface):

    property_name = Attribute('property_name', 'property name for extraction from context')

    def getSkinName():
        """ Returns a skin name from context object. """

    def setSkinName(value):
        """ Set a value in skin name property if last exists """

class IRequestPortalUrlAnnotator(Interface):

    key = Attribute('key', 'Key for saving in request annotations')

    def annotate(value):
        """ Set portal_url sufix in request's annotation to value. """

    def getPortalUrlSuffix():
        """ Extract portal_url suffix from request's annotation by 'key' key. """