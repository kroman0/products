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

    def results():
        """ Return list of dictionary objects
            which confirm Sitemap conditions
        """

    def getAdditionalURLs():
        """ Return additional URL list
        """

    def updateRequest():
        """ Add compression header to RESPONSE
            if allowed
        """


class CommonSitemapView(BrowserView):
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

    def getFilteredObjects(self):
        return []

    def getExceptionResults(self):
        return []

    def results(self):
        try:
            objects = self.getFilteredObjects()
        except AttributeError:
            # We are run without being properly installed, do default processing
            return self.getExceptionResults()

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
