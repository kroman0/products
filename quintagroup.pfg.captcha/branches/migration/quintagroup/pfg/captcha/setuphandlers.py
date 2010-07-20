import logging
from zope.component import queryMultiAdapter

from quintagroup.canonicalpath.interfaces  import ICanonicalLink
from quintagroup.canonicalpath.adapters import PROPERTY_LINK

logger = logging.getLogger('quintagroup.pfg.captcha')

def isNeedMigration(plone_tools):
    ptypes = plone_tools.types()
    cftype = getattr(ptypes, 'CaptchaField', None)
    return cftype and getattr(cftype, 'product', "") == "qPloneCaptchaField"

def migrateToPackage(context):
    """ Replace old qPloneCaptchaField with new quintagroup.pfg.captcha ob.
    """
    if context.readDataFile('_uninstall.txt') is None:
        return
    site = context.getSite()
    plone_tools = queryMultiAdapter((site, setuptool.REQUEST), name="plone_tools")

    if isNeedMigration(plone_tools):
        pass
        ## Find old objects: 
        #for cf in catalog.search({'portal_type':'CaptchaField'}):
        #   get parent obj, del old CaptchaField and create new one 
        # Then remove old portal type "CaptchaField"
        # for path in plone_tools.catalog().search()
        # recriateCaptchaFields(plone_tools)
        # removeOldPortalType(plone_tools)
