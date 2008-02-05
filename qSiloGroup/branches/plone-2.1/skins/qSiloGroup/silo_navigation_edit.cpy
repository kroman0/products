## Controller Python Script "silo_navigation_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##title=Update Folder Property
##parameters= menu_ids=''
#

from Products.CMFCore.utils import getToolByName
from Products.qSiloGroup.utils import isStructuralFolder, getDefaultPage

silo_items = []
for id in menu_ids:
    default_page = ''
    if getattr(context.aq_explicit, id, None):
        item = getattr(context.aq_explicit, id)
    else:
        continue
    if isStructuralFolder(item):
        ids = {}
        for i in item.objectIds():
                ids[i] = 1
        page = getDefaultPage(item)
        if page and ids.has_key(page):
            default_page = page
        if default_page == '':
            site_properties = getToolByName(context, 'portal_properties').site_properties
            for page in site_properties.getProperty('default_page', []):
                if page and ids.has_key(page):
                    default_page = page
                    break
    silo_items.append(id+'|'+default_page+'|'+context.REQUEST.get(id+'_title',''))
if context.hasProperty('silo_items'):
    context.manage_changeProperties({'silo_items': silo_items})
else:
    context.manage_addProperty('silo_items', silo_items, type='lines')

return state.set(status='success', portal_status_message='Silo Navigation property have been saved.')
