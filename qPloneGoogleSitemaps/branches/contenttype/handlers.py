from zope.component import adapter
from Products.CMFCore.utils import getToolByName
#from Products.qPloneGoogleSitemaps.events import AfterTransitionEvent
from Products.qPloneGoogleSitemaps.interfaces import IAfterTransitionEvent
from Products.qPloneGoogleSitemaps.utils import ping_google

@adapter(IAfterTransitionEvent)
def pingGoogle(event):
    object = event.object
    catalog = getToolByName(object, 'portal_catalog')

    sitemaps = [b.getObject() for b in catalog(portal_type='Sitemap')]
    if sitemaps:
        plone_home = getToolByName(object, 'portal_url').getPortalObject().absolute_url()
        wftrans_name = "%s#%s" % (event.workflow.id, event.transition.id)
        for sm in sitemaps:
            if wftrans_name in sm.getPingTransitions():
                ping_google(plone_home, sm.id)
                print "Pinged %s sitemap to google" % sm.id
    return 0
