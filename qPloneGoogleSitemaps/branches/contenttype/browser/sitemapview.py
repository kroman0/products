from commonview import *

class SitemapView(CommonSitemapView):
    """
    Sitemap browser view
    """
    implements(ISitemapView)

    def getFilteredObjects(self):
        path = self.portal.getPhysicalPath()
        portal_types = self.context.getPortalTypes()
        review_states = self.context.getStates()
        return self.portal_catalog(path = path,
                portal_type = portal_types,
                review_state = review_states)

    def getExceptionResults(self):
        path = self.portal.getPhysicalPath()
        return applyOperations(
            self.portal_catalog(path = path,
                                review_state = ['published'],),
            [])
