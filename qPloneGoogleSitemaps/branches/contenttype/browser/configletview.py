from zope.component import queryMultiAdapter
from zope.interface import implements, Interface, Attribute

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.qPloneGoogleSitemaps import qPloneGoogleSitemapsMessageFactory as _
from Products.qPloneGoogleSitemaps.interfaces import ISitemap

def splitNum(num):
    res = []
    prefn = 3
    for c in str(num)[::-1]:
        res.insert(0,c)
        if not len(res)%prefn:
            res.insert(0,',')
            prefn += 4
    return "".join(res[0]==',' and res[1:] or res)

class IConfigletSettingsView(Interface):
    """
    Sitemap view interface
    """

    sitemaps = Attribute("return mapping of sitemap's type to list of appropriate objects")
    hasContentSM = Attribute("Return boolean about existance content sitemap")
    hasMobileSM = Attribute("Return boolean about existance mobile sitemap")
    hasNewsSM = Attribute("Return boolean about existance news sitemap")
    sm_types = Attribute("List of sitemap typs")

    def sitemapsDict(smtype):
        """ Return dictionary like object with data for table
        """

class ConfigletSettingsView(BrowserView):
    """
    Configlet settings browser view
    """
    implements(IConfigletSettingsView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

        catalog = getToolByName(self.context, 'portal_catalog')
        self.sitemaps = [i.getObject() for i in catalog(portal_type='Sitemap')]


    @property
    def sm_types(self):
        return [i.getSitemapType() for i in self.sitemaps]

    @property
    def hasContentSM(self):
        return 'content' in self.sm_types

    @property
    def hasMobileSM(self):
        return 'mobile' in self.sm_types

    @property
    def hasNewsSM(self):
        return 'news' in self.sm_types

    @property
    def sitemapsDict(self):
        content, mobile, news = [],[],[]
        for sm in self.sitemaps:
            data = self.getSMData(sm)
            if data['sm_type'] == 'Content':
                content.append(data)
            elif data['sm_type'] == 'Mobile':
                mobile.append(data)
            elif data['sm_type'] == 'News':
                news.append(data)
        return content + mobile + news

    def getSMData(self, ob):
        size, entries = self.getSitemapData(ob)
        return {'sm_type'    : ob.getSitemapType().capitalize(),
                'sm_id'      : ob.id,
                'sm_url'     : ob.absolute_url(),
                'sm_size'    : size and splitNum(size) or '',
                'sm_entries' : entries and splitNum(entries) or '',
               }

    def getSitemapData(self, ob):
        size, entries = (0, 0)
        view = ob and ob.defaultView() or None
        if view:
            resp = self.request.RESPONSE
            bview = queryMultiAdapter((ob,self.request), name=view)
            if bview:
                try:
                    size = len(bview())
                    entries = bview.numEntries
                    self.request.RESPONSE.setHeader('Content-Type', 'text/html')
                except:
                    pass
        return (size, entries)
