""" Utility functions """

from zope.component import getMultiAdapter

from OFS.DTMLMethod import addDTMLMethod

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.migrations.migration_util import safeEditProperty
from Products.CMFCore.Expression import Expression, createExprContext

from config import PROPERTY_FIELD, PROPERTY_SHEET

def addCSS(container, sheetId, title, csshovering):
    """ Add DTML Method object to portal root """
    addDTMLMethod(container, sheetId, title, csshovering)

def updateMenu(site):
    pu = getToolByName(site, 'plone_utils')
    pa = getToolByName(site, 'portal_actions')
    portal_props = getToolByName(site, 'portal_properties')

    # collect all portal tabs
    context_state = getMultiAdapter((site, site.REQUEST), name=u'plone_context_state')
    actions = context_state.actions()
    portal_tabs_view = getMultiAdapter((site, site.REQUEST), name='portal_tabs_view')
    portal_tabs = portal_tabs_view.topLevelTabs(actions=actions)

    # dump to html
    value = ''
    for tab in portal_tabs:
        value += '<li id="portaltab-%s" class="plain">\n' % tab['id']
        value += '  <a href="%s" accesskey="t" title="%s">%s</a>\n' % (tab['url'], tab['description'], tab['name'])
        value += '</li>\n'

    if not hasattr(portal_props.aq_base, PROPERTY_SHEET):
        portal_props.addPropertySheet(PROPERTY_SHEET, 'DropDown Menu Properties')
    ap = getattr(portal_props.aq_base, PROPERTY_SHEET)
    safeEditProperty(ap, PROPERTY_FIELD, value, 'text')
