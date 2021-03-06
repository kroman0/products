import sys
import logging
from zope.component import queryUtility
from zope.component import getSiteManager
from zope.component import getGlobalSiteManager
from plone.registry.interfaces import IRegistry
from plone.browserlayer.utils import unregister_layer
from plone.browserlayer.interfaces import ILocalBrowserLayerType

from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName

from quintagroup.dropdownmenu.interfaces import IDropDownMenuSettings
from quintagroup.dropdownmenu import PROJECT_NAME, logger


def removeConfiglet(site):
    """ Remove configlet.
    """
    conf_id = "dropdownmenu"
    controlpanel_tool = getToolByName(site, 'portal_controlpanel')
    if controlpanel_tool:
        controlpanel_tool.unregisterConfiglet(conf_id)
        logger.log(logging.INFO, "Unregistered \"%s\" configlet." % conf_id)

def cleanupRegistry(site):
    registry = queryUtility(IRegistry)
    iprefix = IDropDownMenuSettings.__identifier__ + '.'
    delrecs = [r for r in registry.records.keys() if r.startswith(iprefix)]
    map(registry.records.__delitem__, delrecs)
    logger.log(logging.INFO, "Removed %s items from plone.app.registry" % delrecs)

def fixQIUninstallDependencies(site):
    """Uninstallation procedure of Quickinstaller tool clean-up settings,
       made by dependent products. Fix this issue.
    """
    qi = getToolByName(site, 'portal_quickinstaller')
    qiprod = getattr(qi, PROJECT_NAME, None)
    if qiprod:
        utilities = getattr(qiprod, 'utilities', [])
        todel = filter(lambda k:not sum(map(lambda i:PROJECT_NAME in i, k)), utilities)
        for u in todel:
            uidx = utilities.index(u)
            del utilities[uidx]

def uninstall(context):
    """ Do customized uninstallation.
    """
    if context.readDataFile('quintagroup_dropdownmenu_uninstall.txt') is None:
        return

    site = context.getSite()
    fixQIUninstallDependencies(site)
    removeConfiglet(site)
    cleanupRegistry(site)

