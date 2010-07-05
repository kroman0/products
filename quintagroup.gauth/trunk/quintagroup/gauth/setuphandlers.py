import logging

from zope.component import getSiteManager
from Products.CMFCore.utils import getToolByName

from quintagroup.gauth.utility import GAuthUtility
from quintagroup.gauth.interfaces import IGAuthUtility

logger = logging.getLogger('quintagroup.gauth')

def registerGAuthUtility(context):
    """ Register Google Authentication utility
    """
    if context.readDataFile('quintagrouop_gauth.txt') is None:
        return

    site = context.getSite() 
    sm = getSiteManager(site)
    gauth = GAuthUtility(site)
    sm.registerUtility(component=gauth,
                       provided=IGAuthUtility)
    logger.log(logging.INFO, "Registered IGAuthUtility, bound it to the site.")


def uninstallStuff(context):
    if context.readDataFile('quintagroup_gauth_unisntall.txt') is None:
        return

    site = context.getSite() 
    unregisterUtility(site)
    removeGauthProperties(site)
    removeConfiglet(site)
    removeActionIcons(site)

def unregisterUtility(site):
    sm = getSiteManager(site)
    existing = queryUtility(IGAuthUtility)
    if existing is None:
        logger.log(logging.WARN, "No GAuthUtility is registered.")

    sm.unregisterUtility(component=existing, provided=IGAuthUtility)
    logger.log(logging.INFO, "Unregistered IGAuthUtility, from local sitemanager.")    

def removeGauthProperties(site):
    pp = getToolByName(site, "portal_properties")
    if not "gauth_properties" in pp.objectIds():
        logger.log(logging.WARN, "No 'gauth_properties' present in portal_properties.")
    pp.manage_delObjects(ids="gauth_properties")
    logger.log(logging.INFO, "Removed 'gauth_properties' from portal_properties.")

def removeConfiglet(site):
    pcp = getToolByName(site, "portal_controlpanel")
    if not "quintagroup.gauth" in pcp.objectIds():
        logger.log(logging.WARN, "No 'quintagroup.gauth' configlet.")
    pcp.unregisterConfiglet("quintagroup.gauth")
    logger.log(logging.INFO, "Removed 'quintagroup.gauth' configlet.")
    
def removeActionIcons(site):
    pai = getToolByName(site, "portal_actionicons")
    if not "quintagroup.gauth" in pai.objectIds():
        logger.log(logging.WARN, "No 'quintagroup.gauth' configlet.")

    pai.manage_removeActionIcon(category="controlpanel", action_id="quintagroup.gauth")
    logger.log(logging.INFO, "Removed 'quintagroup.gauth' action icon.")
