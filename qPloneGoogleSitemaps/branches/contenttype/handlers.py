from urllib2 import urlopen
from urllib  import quote as urlquote

from zope.component import adapter
from Products.CMFCore.utils import getToolByName
from Products.qPloneGoogleSitemaps.events import AfterTransitionEvent
from Products.qPloneGoogleSitemaps.interfaces import IAfterTransitionEvent
from Products.qPloneGoogleSitemaps.utils import ping_google

def pingByType(event, smtype):
    object = event.object
    portal = getToolByName(object, 'portal_url').getPortalObject()
    pp = getToolByName(object, 'portal_properties')
    props = getattr(pp, 'googlesitemap_properties', None)

    pname = "%s_default" % smtype
    csm_path = props and props.getProperty(pname, '') or ''
    if csm_path:
        csm = portal.unrestrictedTraverse(csm_path, default=None)
        wftrans_name = "%s#%s" % (event.workflow.id, event.transition.id)
        if csm and wftrans_name in csm.getPingTransitions():
            plone_home = getToolByName(object, 'portal_url').getPortalObject().absolute_url()
            ping_google(plone_home, csm.id)
            print "Pinged %s sitemap to google" % smtype


@adapter(IAfterTransitionEvent)
def pingGoogle(event):
    for smtype in ['content', 'mobile', 'news']:
        pingByType(event, smtype)
    return 0
