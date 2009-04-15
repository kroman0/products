from zope.interface import alsoProvides, noLongerProvides

from quills.app.utilities import recurseToInterface
from quills.core.interfaces import IWeblogEnhanced
from quills.core.interfaces.enabled import IPossibleWeblogEntry

from Products.CMFCore.utils import getToolByName

from quintagroup.quills.extras.browser.interfaces import IWeblogCategory
from zope.component import getSiteManager

def set_layout(sc_info):
    #portal = sc_info.getPortal()
    obj = sc_info.object
    weblog = recurseToInterface(obj, IWeblogEnhanced)
    if weblog:
        updateBlogPost(obj)

def updateBlogPost(obj):
    # set default layout
    obj.setLayout('weblogentry_view')
    # add providing of IPossibleWeblogEntry interface
    if not IPossibleWeblogEntry.providedBy(obj):
        alsoProvides(obj, IPossibleWeblogEntry)
    # allow discussion for object
    dt = getToolByName(obj,'portal_discussion')
    dt.overrideDiscussionFor(obj, 1)

def processBlog(self, path, blogentry_types=["Document",]):
    catalog = getToolByName(self,'portal_catalog')
    brains = catalog(path=path, portal_type=blogentry_types)
    for b in brains:
        obj = b.getObject()
        updateBlogPost(obj)
        print b.getURL(), 'updated'
    #raise Exception("some error")


def processBlogSubFolders(self):
    # update blog sub-folders
    res = []
    brains = self.portal_catalog(path='/'.join(self.getPhysicalPath()),
                                 portal_type=['Large Plone Folder','Folder'])
    context_path = '/'.join(self.getPhysicalPath())
    brains = filter(lambda b:not b.getPath()==context_path, brains)
    for bf in brains:
        item_res = [bf.getPath(),0,0]
        ob = bf.getObject()
        if ob.hasProperty('layout'):
            ob.manage_delProperties(['layout',])
        ob.manage_addProperty('layout','weblogfolder_view','string')
        if IWeblogEnhanced.providedBy(ob):
            noLongerProvides(ob,IWeblogEnhanced)
            item_res[1] = 1
        if not IWeblogCategory.providedBy(ob):
            alsoProvides(ob,IWeblogCategory)
            item_res[2] = 1
        res.append(item_res)
    return res


from zope.interface import Interface
from Products.CMFPlone.SyndicationTool import SyndicationTool
from Products.CMFCore.interfaces import ISyndicationTool
from vice.outbound.feedsettings import FeedSettings
from zope.component import queryUtility
from vice.outbound.interfaces import IFeedSettings


from plone.browserlayer.interfaces import ILocalBrowserLayerType

def restoreSyndication(self):
    site = self.portal_url.getPortalObject()
    sm = getSiteManager(self)
    sm.unregisterUtility(provided=ISyndicationTool)
    site._delObject("portal_syndication")
    site._setObject("portal_syndication", SyndicationTool())
    sm.registerUtility(site["portal_syndication"].aq_base, provided=ISyndicationTool)#, name='portal_syndication')
    site["portal_syndication"].editProperties(isAllowed=True)
    
    # unregister utilities
    feedSettings = queryUtility(IFeedSettings)
    sm.unregisterUtility(component=feedSettings, provided=IFeedSettings)

    ploneOutbound = queryUtility(ILocalBrowserLayerType, name="vice.plone.outbound")
    sm.unregisterUtility(component=ploneOutbound, 
                         provided=ILocalBrowserLayerType,
                         name="vice.plone.outbound")

    return "done"

