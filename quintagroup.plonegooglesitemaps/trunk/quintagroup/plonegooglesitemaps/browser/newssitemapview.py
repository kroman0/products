import re
from DateTime import DateTime
from zope.component import getMultiAdapter
from plone.memoize.view import memoize
from quintagroup.plonegooglesitemaps.browser.commonview import *

reTrailingParenthtical = re.compile("\s*\(.*\)\s*", re.S)

class NewsSitemapView(CommonSitemapView):
    """
    News Sitemap browser view
    """
    implements(ISitemapView)

    @property
    def additional_maps(self):
        return (
            ('publication_date', lambda x:DateTime(x.EffectiveDate).strftime("%Y-%m-%d")),
            ('keywords', lambda x:', '.join(x.Subject)),
            ('title', lambda x:x.Title or x.getId or x.id),
            ('name', lambda x:reTrailingParenthtical.sub("",x.Title)),
            ('language', lambda x:x.Language or self.default_language()),
            ('access', lambda x:x.gsm_access or ""),
            ('genres', lambda x:x and ", ".join(x.gsm_genres) or ""),
            ('stock', lambda x:x.gsm_stock or ""),
        )

    @memoize
    def default_language(self):
        pps = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        return pps.default_language

    def getFilteredObjects(self):
        min_date = DateTime() - 3
        return self.portal_catalog(
            path = self.search_path,
            portal_type = self.context.getPortalTypes(),
            review_state = self.context.getStates(),
            effective = {"query": min_date,
                         "range": "min" }
            )
