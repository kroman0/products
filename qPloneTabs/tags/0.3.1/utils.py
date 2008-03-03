"""
   Utility functions for portal_tab actions modifications.
"""
from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName

def getPortalActions(self, category='portal_tabs'):
    """ Return all portal actions with 'portal_tabs' category """
    return filter(lambda a: a.category == category, getToolByName(self, 'portal_actions')._cloneActions())

def editAction(self, num, name, id, action='', condition='', visibility=[], category='portal_tabs'):
    """ Function for editing given action """
    actions = getToolByName(self, 'portal_actions')._actions
    tabs = filter(lambda a: a.category == category, actions)
    tab = tabs[int(num)]
    if visibility != []:
        if visibility == 'true': visibility = True
        else: visibility = False
        tab.visible = visibility
        return 'Changed visibility'
    if id: tab.id = id
    if name: tab.title = name
    if isinstance(condition, basestring): tab.condition = Expression(condition)
    if isinstance(action, basestring): tab.setActionExpression(Expression(action))
    return True

def reorderActions(self, idxs, category='portal_tabs'):
    """ Reorder portal_tabs actions in given order """
    idxs = list(map(int,idxs))
    portal_actions = getToolByName(self, 'portal_actions')
    actions = portal_actions._cloneActions()
    tabs = [[action, actions.index(action)] for action in actions if action.category == category]
    for idx in range(len(idxs)):
        actions[tabs[idx][1]] = tabs[idxs[idx]][0]
    portal_actions._actions = tuple(actions)
    return idxs

def deleteAction(self, idx, id, category='portal_tabs'):
    """ Delete portal_tabs action with given index """
    portal_actions = getToolByName(self, 'portal_actions')
    actions = portal_actions._cloneActions()
    tabs = filter(lambda a: a.category == category, actions)
    if tabs[int(idx)].id == id:
        portal_actions.deleteActions([actions.index(tabs[int(idx)]),])
    return id

def processUrl(self, url):
    """ Return url in a right format """
    import re
    if url.find('/') == 0: return 'string:${portal_url}' + url
    elif re.compile('^(ht|f)tps?\:', re.I).search(url): return 'string:' + url
    elif re.compile('^(python:|string:|not:|exists:|nocall:|path:)', re.I).search(url): return url
    else: return 'string:${object_url}/' + url

def getRootTabs(self):
    """ Return all portal root elements which are displayed in poral globalnav """
    stp = getToolByName(self, 'portal_properties').site_properties
    if stp.getProperty('disable_folder_sections', True):
        return []
    result = []
    query = {}
    portal_path = getToolByName(self, 'portal_url').getPortalPath()
    query['path'] = {'query':portal_path, 'navtree':1}
    utils = getToolByName(self, 'plone_utils')
    ct = getToolByName(self, 'portal_catalog')
    ntp = getToolByName(self, 'portal_properties').navtree_properties
    views = stp.getProperty('typesUseViewActionInListings', ())
    query['portal_type'] = utils.typesToList()
    if ntp.getProperty('sortAttribute', False):
        query['sort_on'] = ntp.sortAttribute
    if (ntp.getProperty('sortAttribute', False) and ntp.getProperty('sortOrder', False)):
        query['sort_order'] = ntp.sortOrder
    if ntp.getProperty('enable_wf_state_filtering', False):
        query['review_state'] = ntp.wf_states_to_show
    query['is_default_page'] = False
    query['is_folderish'] = True
    excluded_ids = {}
    for exc_id in ntp.getProperty('idsNotToList', ()):
        excluded_ids[exc_id] = 1
    rawresult = ct(**query)
    for item in rawresult:
        if not excluded_ids.has_key(item.getId):
            item_url = (item.portal_type in views and item.getURL() + '/view') or item.getURL()
            data = {'name' : utils.pretty_title_or_id(item),
                    'id' : item.getId,
                    'url' : item_url,
                    'description' : item.Description,
                    'exclude_from_nav' : item.exclude_from_nav}
            result.append(data)
    return result