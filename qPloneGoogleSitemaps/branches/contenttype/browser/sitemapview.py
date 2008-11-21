from string import find
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.qPloneGoogleSitemaps import qPloneGoogleSitemapsMessageFactory as _
from utils import additionalURLs, applyOperations


class ISitemapView(Interface):
    """
    Sitemap view interface
    """

    def test():
        """ test method"""


class SitemapView(BrowserView):
    """
    Sitemap browser view
    """
    implements(ISitemapView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}

    def results(self, path=None):
        if not path:
            portal = getToolByName(self.context, 'portal_url')
            path = portal.getPortalPath()

        portal_types = self.context.getPortalTypes()
        review_states = self.context.getStates()
        catalog = getToolByName(self.context, 'portal_catalog')
        try:
            objects = catalog(path = path,
                portal_type = portal_types,
                review_state = review_states,)
        except AttributeError:
            # We are run without being properly installed, do default processing
            return applyOperations(catalog(path = path,
                review_state = ['published'],), [])

        blackout_list = self.context.getBlackout_list()
        reg_exps = self.context.getReg_exp()
        return applyOperations([ob for ob in objects 
            if (ob.getId not in blackout_list)],
            reg_exps)

    def updateRequest(self):
        self.request.RESPONSE.setHeader('Content-Type', 'text/xml')
        try:
            compression = self.context.enableHTTPCompression()
            if compression:
                compression(request=self.request)
        except:
            pass

    def getAdditionalURLs(self):
        return additionalURLs(self.context)
