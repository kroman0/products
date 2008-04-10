from zope.dottedname.resolve import resolve
from zope.component import getUtility, getSiteManager, getMultiAdapter

from plone.portlets.interfaces import IPortletAssignmentMapping, IPortletManager, IPlacelessPortletManager
from plone.portlets.interfaces import IPortletContext, IPortletDataProvider
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.storage import PortletCategoryMapping, PortletAssignmentMapping
from plone.app.portlets import portlets

from plone.app.customerize.registration import *

from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.utils import _getDottedName, _resolveDottedName

from Products.%(product_name)s.config import *
from Products.%(product_name)s.utils import *
from Products.%(product_name)s.setuphandlers import setupSiteWidePortlets
from Products.%(product_name)s.setuphandlers import setupPortletsForContext

import sys
from logging import getLogger
logger = getLogger('%(product_name)s:unistall')

_marker = []


def uninstallPortlets(context):
    if context.readDataFile('%(uninstall_profile_marker)s') is None:
        return

    site = context.getSite()

    components = getSiteManager(site)
    ms = [r for r in components.registeredUtilities() if r.provided.isOrExtends(IPortletManager)]
    context_managers = {}
    for m in ms:
        if not m.provided.isOrExtends(IPlacelessPortletManager):
            context_managers[m.name] = getUtility(IPortletManager, name=m.name, context=site)

    managers = {}
    for m in ms:
        managers[m.name] = getUtility(IPortletManager, name=m.name, context=site)

    # initiate list for collect blacklist properties
    pp = getToolByName(site, 'portal_properties')
    estate_props = getattr(pp, '%(product_name_lowercase)s_properties', None)
    slots_structure_before_install = estate_props.getProperty('portlets_before_install',"[]")
    slots_info = eval(slots_structure_before_install)

    for path, info in slots_info:
        if path == '__site-wide-portlets__':
            setupSiteWidePortlets(site, info, managers)
        else:
            try:
                obj = site.restrictedTraverse(path)
            except:
                e,v,tr = sys.exc_info()
                logger.info('Debug from importPortlets handler: %%s: %%s (%%s)' , path, str(v), str(e))
            else:
                setupPortletsForContext(obj, info, context_managers)


def uninstallProperties(context):
    if context.readDataFile('%(uninstall_profile_marker)s') is None:
        return

    site = context.getSite()
    portal_properties = getToolByName(site, 'portal_properties')
    
    if '%(product_name_lowercase)s_properties' in portal_properties.objectIds():
           portal_properties.manage_delObjects(ids=['%(product_name_lowercase)s_properties',])

