import re
from DateTime import DateTime
from commonview import *
from zope.component import getMultiAdapter

reTrailingParenthtical = re.compile("\s*\(.*\)\s*", re.S)

class NewsSitemapView(CommonSitemapView):
    """
    News Sitemap browser view
    """
    implements(ISitemapView)

    additional_maps = (
        ('publication_date', lambda x:DateTime(x.EffectiveDate).strftime("%Y-%m-%d")),
        ('keywords', lambda x:', '.join(x.Subject)),
        ('name', lambda x:reTrailingParenthtical.sub("",x.Title)),
        ('title', lambda x:x.Title),
        ('language', lambda x:x.Language),
        ('access', lambda x:x.gsm_access),
        ('genres', lambda x:x.gsm_genres),
    )

    def getFilteredObjects(self):
        path = self.portal.getPhysicalPath()
        portal_types = self.context.getPortalTypes()
        review_states = self.context.getStates()
        min_date = DateTime() - 3
        res = self.portal_catalog(path = path,
                portal_type = portal_types,
                review_state = review_states,
                effective = {"query": min_date,
                             "range": "min" })
        return res
