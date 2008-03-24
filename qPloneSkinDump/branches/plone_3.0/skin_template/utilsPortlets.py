from zope.interface import providedBy
from zope.schema import getFields
from zope.component import getMultiAdapter, getUtility, getSiteManager

from plone.portlets.interfaces import IPortletAssignmentMapping, IPortletManager, IPlacelessPortletManager
from plone.portlets.interfaces import IPortletContext, IPortletDataProvider
from plone.portlets.interfaces import ILocalPortletAssignmentManager

from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.utils import _getDottedName, _resolveDottedName


def extractInfoFromAssignment(name, assignment):
    klass = assignment.__class__
    a = {'name' : name, 'class' : '%s' % _getDottedName(klass)}
    data = assignment.data
    kwargs = {}
    for i in list(providedBy(data)):
        if i.isOrExtends(IPortletDataProvider):
            for field_name, field in getFields(i).items():
                kwargs[field_name] = field.get(assignment)
    a['kwargs'] = kwargs
    return a

def extractSiteWidePortlets(context, managers):
    """ Extract site-wide portlets 
        Data structure:
            '__site-wide-portlets__', [(<manager1_name>, <manager1_info>),
                                       (<manager2_name>, <manager2_info>),
                                       (<manager3_name>, <manager3_info>)])
            <manager_info>:
                {'category1' : <catmapping1>,
                 'category2' : <catmapping2>}
            <catmapping>:
                {'key1' : <mapping1>,
                 'key2' : <mapping2>}
            <mapping>:
                {'assignment_name1' : <assignment1>,
                 'assignment_name2' : <assignment2>}
            <assignment>:
                {'name'   : 'Assignment',
                 'class'  : 'dotted.path.to.assignment.class',
                 'kwargs' : {'parameter1' : 'value1',
                             'parameter2' : 'value2'}
    """
    info = []
    for manager_name, manager in managers:
        manager_info = {}
        for category, catmapping in manager.items():
            catmapping_info = {}
            for key, mapping in catmapping.items():
                mapping_info = {}
                for name, assignment in mapping.items():
                    mapping_info[name] = extractInfoFromAssignment(name, assignment)
                catmapping_info[key] = mapping_info
            manager_info[category] = catmapping_info
        info.append((manager_name, manager_info))
    return info

def extractContextPortletsFromManager(context, manager):
    """ Extract all contextual portlets from given object and portlet manager, and portlets blacklists
        Data structure:
        <manager_info> =
            {'blacklists'  : [(GROUP_CATEGORY, True),
                              (CONTENT_TYPE_CATEGORY, False),
                              (CONTEXT_CATEGORY, None)],
             'assignments' : [{'name'   : 'Assignment-2',
                               'class'  : 'dotted.path.to.assignment.class',
                               'kwargs' : {'parameter1' : 'value1',
                                          'parameter2' : 'value2'}},
                              {'name'   : 'Assignment',
                               'class'  : 'dotted.path.to.assignment.class',
                               'kwargs' : {'parameter1' : 'value1',
                                            'parameter2' : 'value2'}]}
    """

    info = {}
    info['assignments'] = assignments = []
    info['blacklists'] = blacklists = []

    # Extract contextual portlets
    mapping = getMultiAdapter((context, manager), IPortletAssignmentMapping, context=context)
    for name, assignment in mapping.items():
        assignments.append(extractInfoFromAssignment(name, assignment))

    # Extract blacklists for given object and manager
    localassignmentmanager = getMultiAdapter((context, manager), ILocalPortletAssignmentManager)
    blacklist = localassignmentmanager._getBlacklist()
    if blacklist is not None:
        for category, key in blacklist.items():
            blacklists.append((category, key))

    return info

def extractPortletsFromContext(context, slot_structure, typesToShow, managers):
    """ Extract portlets for given object assigned through all portlet managers.
        Data structure:
            ('unique/path/to/context', [(<manager1_name>, <manager1_info>),
                                        (<manager2_name>, <manager2_info>),
                                        (<manager3_name>, <manager3_info>)])
    """


    info = []
    key = '/'.join(context.getPhysicalPath()[2:])

    for name, manager in managers:
        info.append((name, extractContextPortletsFromManager(context, manager)))

    slot_structure.append((key, info))

    return slot_structure

def dumpAllPortlets(context, slot_structure, typesToShow, managers):
    extractPortletsFromContext(context, slot_structure, typesToShow, managers)
    if getattr(context.aq_base, 'isPrincipiaFolderish', 0):
        for id, obj in context.contentItems():
            if obj.portal_type in typesToShow:
                dumpAllPortlets(obj, slot_structure, typesToShow, managers)

    return slot_structure

def dumpPortlets(context, dump_policy, dump_portlets_selection):
    """ Extract portlets from given set of objects and site-wide portlets too.
        Data structure:
            SLOT_STRUCTURE =
                [(), (), ()]
    """

    portal = getToolByName(context, 'portal_url').getPortalObject()
    portal_state = getMultiAdapter((portal, context.REQUEST), name=u'plone_portal_state')
    typesToShow = portal_state.friendly_types()

    components = getSiteManager(context)
    managers = [r for r in components.registeredUtilities() if r.provided.isOrExtends(IPortletManager)]
    context_managers = [(m.name, getUtility(IPortletManager, name=m.name, context=context)) for m in managers
                                                                               if not IPlacelessPortletManager.providedBy(m.component)]
    managers = [(m.name, getUtility(IPortletManager, name=m.name, context=context)) for m in managers]

    slot_structure = []
    if dump_policy == 'root':
        extractPortletsFromContext(portal, slot_structure, typesToShow, context_managers)
    elif dump_policy == 'all':
        dumpAllPortlets(portal, slot_structure, typesToShow, context_managers)
    elif dump_policy == 'selection':
        for ppath in dump_portlets_selection:
            obj = portal.restrictedTraverse(ppath)
            extractPortletsFromContext(obj, slot_structure, typesToShow, context_managers)

    slot_structure.append(('__site-wide-portlets__', extractSiteWidePortlets(portal, managers)))

    return slot_structure

