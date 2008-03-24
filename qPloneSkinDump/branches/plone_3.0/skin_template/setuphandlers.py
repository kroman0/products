import sys
from logging import getLogger

from BTrees.OOBTree import OOBTree
from persistent.list import PersistentList

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
from Products.%(product_name)s.utilsPortlets import dumpPortlets

logger = getLogger('%(product_name)s')

def assignPortlet(mapping, info):
    name = info['name']
    try:
        assignment = _resolveDottedName(info['class'])
    except:
        e,v,tr = sys.exc_info()
        logger.info('Debug from setup portlets handler: %%s: %%s (%%s)' , info['class'], str(v), str(e))
        return False
    else:
        portlet = assignment(**info['kwargs'])
        if mapping.get(name, None) is not None:
            del mapping[name]
        mapping[name] = portlet
        return portlet

def setupSiteWidePortlets(site, data, managers):

    for name, info in data:
        manager = managers.get(name, None)
        if manager is not None:
            for category, keys in info.items():
                catmapping = manager.get(category, None)
                if catmapping is None:
                    catmapping = manager[category] = PortletCategoryMapping()
                for key, assignments in keys.items():
                    mapping = catmapping.get(key, None)
                    if mapping is None:
                        mapping = catmapping[key] = PortletAssignmentMapping()
                    for assignment in assignments.values():
                        assignPortlet(mapping, assignment)

def setupPortletsForContext(context, data, managers):

    for name, info in data:
        manager = managers.get(name, None)
        if manager is not None:
            # set portlet assignments
            mapping = getMultiAdapter((context, manager), IPortletAssignmentMapping, context=context)

            # purge mapping
            mapping._data = OOBTree()
            mapping._order = PersistentList()

            if info['assignments']:
                # set portlet assignments
                for assignment in info['assignments']:
                    assignPortlet(mapping, assignment)
            if info['blacklists']:
                # set blacklists
                localassignmentmanager = getMultiAdapter((context, manager), ILocalPortletAssignmentManager, context=context)
                for category, status in info['blacklists']:
                    localassignmentmanager.setBlacklistStatus(category, status)


def saveBeforeInstallPortlets(context):
    # Save information about portlets before installation

    beforeInstall = dumpPortlets(context=context, dump_policy='root', dump_portlets_selection=[] )

    # update properties list
    pp = getToolByName(context, 'portal_properties')
    skin_props = pp._getOb('%(product_name_lowercase)s_properties')
    skin_props._updateProperty('portlets_before_install', str(beforeInstall) )


def importPortlets(context):

    if context.readDataFile("%(afterinstall_profile_marker)s") is None:
        return

    site = context.getSite()

    saveBeforeInstallPortlets(site)

    components = getSiteManager(site)
    ms = [r for r in components.registeredUtilities() if r.provided.isOrExtends(IPortletManager)]
    context_managers = {}
    for m in ms:
        if not m.provided.isOrExtends(IPlacelessPortletManager):
            context_managers[m.name] = getUtility(IPortletManager, name=m.name, context=site)

    managers = {}
    for m in ms:
        managers[m.name] = getUtility(IPortletManager, name=m.name, context=site)

    for path, info in SLOT_STRUCTURE:
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

def importZexps(context):

    if context.readDataFile("%(afterinstall_profile_marker)s") is None:
        return

    site = context.getSite()
    if checkIfImport():
        performImportToPortal(site)

def importVarious(context):

    if context.readDataFile("%(afterinstall_profile_marker)s") is None:
        return

    site = context.getSite()
    out = StringIO()
    if FINAL_CUSTOMIZATION_FUNCTIONS:
        dummy = [func(site, out) for func in FINAL_CUSTOMIZATION_FUNCTIONS]

def importCustomViews(context):

    if context.readDataFile("%(afterinstall_profile_marker)s") is None:
        return

    site = context.getSite()

    for view in CUSTOM_VIEWS:
        for_name = view['for_name']
        view_name = view['view_name']
        type_name = view['type_name']
        kwargs = view['kwargs']

        reg = findTemplateViewRegistration(for_name, type_name, view_name)
        viewzpt_id = str(generateIdFromRegistration(reg))

        container = getUtility(IViewTemplateContainer)
        if viewzpt_id in container.objectIds():
            continue

        attr, pt = findViewletTemplate(reg.factory)
        if pt:
            ptname = basename(pt.filename)
        else:
            ptname = None
        viewzpt = TTWViewTemplate(
            id = viewzpt_id,
            text = kwargs['text'],
            encoding = kwargs['encoding'],
            content_type = kwargs['content_type'],
            view = getViewClassFromRegistration(reg),
            permission = getViewPermissionFromRegistration(reg),
            name = ptname)
        container.addTemplate(viewzpt_id, viewzpt)

        sm = getSiteManager(site)
        sm.registerAdapter(viewzpt, required = reg.required, provided = reg.provided, name = reg.name)
