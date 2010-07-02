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
