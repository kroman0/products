"""
   Utility functions for portal_tab actions modifications.
"""
from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName

def getPortalTabs(self):
    """ Return all portal actions with 'portal_tabs' category """
    return filter(lambda a: a.category == 'portal_tabs', getToolByName(self, 'portal_actions')._cloneActions())

def editAction(self, num, name, id, action='', condition=''):
    """ Function for editing given action """
    actions = getToolByName(self, 'portal_actions')._actions
    tabs = filter(lambda a: a.category == 'portal_tabs', actions)
    tab = tabs[int(num)]
    if id: tab.id = id
    if name: tab.title = name
    if isinstance(condition, basestring): tab.condition = Expression(condition)
    if isinstance(action, basestring): tab.setActionExpression(Expression(action))
    return True

def reorderActions(self, idxs):
    """ Reorder portal_tabs actions in given order """
    idxs = list(map(int,idxs))
    portal_actions = getToolByName(self, 'portal_actions')
    actions = portal_actions._cloneActions()
    tabs = [[action, actions.index(action)] for action in actions if action.category == 'portal_tabs']
    for idx in range(len(idxs)):
        actions[tabs[idx][1]] = tabs[idxs[idx]][0]
    portal_actions._actions = tuple(actions)
    return idxs

def deleteAction(self, idx, id):
    """ Delete portal_tabs action with given index """
    portal_actions = getToolByName(self, 'portal_actions')
    actions = portal_actions._cloneActions()
    tabs = filter(lambda a: a.category == 'portal_tabs', actions)
    if tabs[int(idx)].id == id:
        portal_actions.deleteActions([actions.index(tabs[int(idx)]),])
    return id