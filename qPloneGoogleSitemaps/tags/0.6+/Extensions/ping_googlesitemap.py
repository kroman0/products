from Products.qPloneGoogleSitemaps.utils import ping_google
from Products.CMFCore.utils import getToolByName
def  ping_googlesitemap(state_change):
    """ping sitemap to Google when document has published"""
    plone_home = getToolByName(state_change.object, 'portal_url').getPortalObject().absolute_url()
    ping_google(plone_home)
    return 0 