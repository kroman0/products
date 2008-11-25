from zope.interface import implements, Interface, Attribute

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.qPloneGoogleSitemaps import qPloneGoogleSitemapsMessageFactory as _

class IConfigletSettingsView(Interface):
    """
    Sitemap view interface
    """

    sitemaps = Attribute("return mapping of sitemap's type to list of appropriate objects")

    def sitemapsKeys(self):
        """
        """

    def getSMDataByType(self, smtype):
        """
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

    def getSMDataByType(self, smtype):
        data = self.sitemaps[smtype]
        lpp = len(self.portal.getPhysicalPath())

        default = None
        def_path = getattr(self.GSMPSheet, "%s_default" % smtype, '')
        if def_path:
            default = [sm for sm in data if '/'.join(sm.getPhysicalPath()[lpp:])==def_path]
            default = default and default[0] or None

        return {'smtype_title'      : smtype.capitalize(),
                'sm_list'           : [(sm.id, '/'.join(sm.getPhysicalPath()[lpp:]), 
                                        def_path=='/'.join(sm.getPhysicalPath()[lpp:])) for sm in data],
                'sm_def_id'         : default and default.id or '',
                'sm_def_editurl'    : default and '%s/edit' % default.absolute_url() or ''
               }

