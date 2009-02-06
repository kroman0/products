from zope.interface import alsoProvides

from quills.app.utilities import recurseToInterface
from quills.core.interfaces import IPossibleWeblog
from quills.core.interfaces.enabled import IPossibleWeblogEntry

from Products.CMFCore.utils import getToolByName

def set_layout(sc_info):
    #portal = sc_info.getPortal()
    obj = sc_info.object
    weblog = recurseToInterface(obj, IPossibleWeblog)
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

