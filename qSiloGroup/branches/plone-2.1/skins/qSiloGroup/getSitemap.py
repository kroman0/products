## Script (Python) "getSitemap"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_callable
from Products.CMFCore.WorkflowCore import WorkflowException

def addToNavTreeResult(result, data):
    """Adds a piece of content to the result tree."""
    path = data['path']
    parentpath = '/'.join(path.split('/')[:-1])
    # Tell parent about self
    if result.has_key(parentpath):
        result[parentpath]['children'].append(data)
    else:
        result[parentpath] = {'children':[data]}
    # If we have processed a child already, make sure we register it
    # as a child
    if result.has_key(path):
        data['children'] = result[path]['children']
    result[path] = data

ct = getToolByName(context, 'portal_catalog')
ntp = getToolByName(context, 'portal_properties').navtree_properties
stp = getToolByName(context, 'portal_properties').site_properties
plone_utils = getToolByName(context, 'plone_utils')
view_action_types = stp.getProperty('typesUseViewActionInListings', ())
currentPath = None
portalpath = getToolByName(context, 'portal_url').getPortalPath()

custom_query = getattr(context, 'getCustomNavQuery', None)
if custom_query is not None and safe_callable(custom_query):
    query = custom_query()
else:
    query = {}

currentPath = portalpath
query['path'] = {'query':currentPath,
                 'depth':ntp.getProperty('sitemapDepth', 2)}

query['portal_type'] = plone_utils.typesToList()

if ntp.getProperty('sortAttribute', False):
    query['sort_on'] = ntp.sortAttribute

if (ntp.getProperty('sortAttribute', False) and ntp.getProperty('sortOrder', False)):
    query['sort_order'] = ntp.sortOrder

if ntp.getProperty('enable_wf_state_filtering', False):
    query['review_state'] = ntp.wf_states_to_show

query['is_default_page'] = False

parentTypesNQ = ntp.getProperty('parentMetaTypesNotToQuery', ())

# Get ids not to list and make a dict to make the search fast
ids_not_to_list = ntp.getProperty('idsNotToList', ())
excluded_ids = {}
for exc_id in ids_not_to_list:
    excluded_ids[exc_id] = 1

rawresult = ct(**query)

# Build result dict
result = {}
foundcurrent = False
for item in rawresult:
    path = item.getPath()

    if item.is_folderish:
        default_page = item.getObject().getProperty('default_page', '')
        if default_page:
            item_url = '%s/%s' % (item.getURL(), default_page)
        else:
            item_url = (item.portal_type in view_action_types and item.getURL() + '/view') or item.getURL()
    else:
        item_url = (item.portal_type in view_action_types and item.getURL() + '/view') or item.getURL()

    currentItem = path == currentPath
    if currentItem:
        foundcurrent = path
    no_display = (
        excluded_ids.has_key(item.getId) or
        not not getattr(item, 'exclude_from_nav', True))
    data = {'Title':plone_utils.pretty_title_or_id(item),
            'currentItem':currentItem,
            'absolute_url': item_url,
            'getURL':item_url,
            'path': path,
            'icon':item.getIcon,
            'creation_date': item.CreationDate,
            'portal_type': item.portal_type,
            'review_state': item.review_state,
            'Description':item.Description,
            'show_children':item.is_folderish and item.portal_type not in parentTypesNQ,
            'children':[],
            'no_display': no_display}
    addToNavTreeResult(result, data)

if ntp.getProperty('showAllParents', False):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    parent = context
    parents = [parent]
    while not parent is portal:
        parent = parent.aq_parent
        parents.append(parent)

    wf_tool = getToolByName(context, 'portal_workflow')
    for item in parents:
        if getattr(item, 'getPhysicalPath', None) is None:
            # when Z3-style views are used, the view class will be in
            # the 'parents' list, but will not support 'getPhysicalPath'
            # we can just skip it b/c it's not an object in the content
            # tree that should be showing up in the nav tree (ra)
            continue
        path = '/'.join(item.getPhysicalPath())
        if not result.has_key(path) or not result[path].has_key('path'):
            # item was not returned in catalog search
            if foundcurrent:
                currentItem = False
            else:
                currentItem = path == currentPath
                if currentItem:
                    if plone_utils.isDefaultPage(item):
                        # don't list folder default page
                        continue
                    else:
                        foundcurrent = path
            try:
                review_state = wf_tool.getInfoFor(item, 'review_state')
            except WorkflowException:
                review_state = ''

            if item.is_folderish():
                default_page = item.getProperty('default_page', '')
                if default_page:
                    item_url = '%s/%s' % (item.absolute_url(), default_page)
                else:
                    item_url = (item.portal_type in view_action_types and item.absolute_url() + '/view') or item.absolute_url()
            else:
                item_url = (item.portal_type in view_action_types and item.absolute_url() + '/view') or item.absolute_url()

            data = {'Title': plone_utils.pretty_title_or_id(item),
                    'currentItem': currentItem,
                    'absolute_url': item_url,
                    'getURL': item_url,
                    'path': path,
                    'icon': item.getIcon(),
                    'creation_date': item.CreationDate(),
                    'review_state': review_state,
                    'Description':item.Description(),
                    'children':[],
                    'portal_type':item.portal_type,
                    'no_display': 0}
            addToNavTreeResult(result, data)

if not foundcurrent:
    for i in range(1, len(currentPath.split('/')) - len(portalpath.split('/')) + 1):
        p = '/'.join(currentPath.split('/')[:-i])
        if result.has_key(p):
            foundcurrent = p
            result[p]['currentItem'] = True
            break

if result.has_key(portalpath):
    return result[portalpath]
else:
    return {}