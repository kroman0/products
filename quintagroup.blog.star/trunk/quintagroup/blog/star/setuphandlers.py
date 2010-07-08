import logging

from zope.component import getSiteManager
from plone.browserlayer.utils import unregister_layer
from plone.browserlayer.interfaces import ILocalBrowserLayerType

from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('quintagroup.blog.star')

def removeBrowserLayer(site):
    """ Remove browser layer.
    """
    name="quintagroup.blog.star"
    site = getSiteManager(site)
    registeredLayers = [r.name for r in site.registeredUtilities()
                        if r.provided == ILocalBrowserLayerType]
    if name in registeredLayers:
        unregister_layer(name, site_manager=site)
        logger.log(logging.INFO, "Unregistered \"%s\" browser layer." % name)

def uninstall(context):
    """ Do customized uninstallation.
    """
    if context.readDataFile('quintagroup.blog.star_uninstall.txt') is None:
        return
    site = context.getSite()
    removeBrowserLayer(site)
