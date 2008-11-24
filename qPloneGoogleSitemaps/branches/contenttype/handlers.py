from urllib2 import urlopen
from urllib  import quote as urlquote

from zope.component import adapter
from Products.CMFCore.utils import getToolByName
from Products.qPloneGoogleSitemaps.events import AfterTransitionEvent
from Products.qPloneGoogleSitemaps.interfaces import IAfterTransitionEvent
from Products.qPloneGoogleSitemaps.utils import ping_google

def pingByType(event, smtype):
    object = event.object
    catalog = getToolByName(object, 'portal_catalog')

    csm = None
    for brain in catalog(portal_type='Sitemap'):
        smobj = brain.getObject()
        if smobj.getSitemapType() == smtype:
            csm = smobj
            break
    if csm:
        wftrans_name = "%s#%s" % (event.workflow.id, event.transition.id)
        if wftrans_name in csm.getPingTransitions():
            plone_home = getToolByName(object, 'portal_url').getPortalObject().absolute_url()
            ping_google(plone_home, csm.id)
            print "Pinged %s sitemap to google" % smtype


@adapter(IAfterTransitionEvent)
def pingGoogle(event):
    for smtype in ['content', 'mobile', 'news']:
        pingByType(event, smtype)
    return 0
