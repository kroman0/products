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

    def sitemapsKeys(self):
        """Return sitemap type existent
        """

    def getSMDataByType(self, smtype):
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

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def GSMPSheet(self):
        return getToolByName(self.context, 'portal_properties').googlesitemap_properties

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    @property
    def sitemaps(self):
        sitemaps = {}
        smbrains = self.portal_catalog(portal_type="Sitemap")
        for smbrain in smbrains:
            sm = smbrain.getObject()
            sm_type = sm.getSitemapType()
            sitemap = sitemaps.setdefault(sm_type, [])
            sitemap.append(sm)
        return sitemaps

    def sitemapsKeys(self):
        return self.sitemaps.keys()

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

    def getSMDataByType(self, smtype):
        data = self.sitemaps[smtype]
        lpp = len(self.portal.getPhysicalPath())

        default = None
        def_path = getattr(self.GSMPSheet, "%s_default" % smtype, '')
        if def_path:
            default = [sm for sm in data if '/'.join(sm.getPhysicalPath()[lpp:])==def_path]
            default = default and default[0] or None
        def_size, def_entries = self.getSitemapData(default)
        return {'smtype_title'      : smtype.capitalize(),
                'sm_list'           : [(sm.id, '/'.join(sm.getPhysicalPath()[lpp:]), 
                                        def_path=='/'.join(sm.getPhysicalPath()[lpp:])) for sm in data],
                'sm_def_id'         : default and default.id or '',
                'sm_def_editurl'    : default and '%s/edit' % default.absolute_url() or '',
                'sm_def_size'       : def_size and splitNum(def_size) or '',
                'sm_def_entries'    : def_entries and splitNum(def_entries) or '',
               }
