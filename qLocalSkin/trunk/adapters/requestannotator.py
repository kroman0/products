from zope.interface import implements
from zope.component import adapts
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.annotation.interfaces import IAnnotations

from Products.qLocalSkin.config import ANNOTATION_KEY
from interfaces import IRequestPortalUrlAnnotator

class RequestPortalUrlAnnotator(object):
    """ Adapter for working with portal_url suffix in request's annotation. """

    implements(IRequestPortalUrlAnnotator)
    adapts(IBrowserRequest)

    key = ANNOTATION_KEY

    def __init__(self, request):
        self.request = request
        self.annotations = IAnnotations(self.request, None)

    def annotate(self, value):
        if self.annotations is not None:
            self.annotations[self.key] = value
            # print "################## Setted annotation on request from qLocalSkin: " + str(value)
            return True
        return False

    def getPortalUrlSuffix(self):
        if self.annotations is not None:
            return self.annotations.get(self.key, '')
        return ''
