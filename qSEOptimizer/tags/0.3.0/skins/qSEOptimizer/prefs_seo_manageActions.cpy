## Script (Python) "prefs_seo_config"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= portalTypes= []
##title=add action tab for selected portal types
##
from Products.CMFCore.utils import getToolByName

pt = getToolByName(context, 'portal_types')
for ptype in pt.objectValues():
    action = ptype.getActionById('seo_properties', default=None )

    if ptype.getId() in portalTypes:
        if action is None:
            ptype.addAction('seo_properties',
                            'SEO Properties',
                            'string:${object_url}/qseo_properties_edit_form',
                            '',
                            'Modify portal content',
                            'object',
                            visible=1)
    else:
        if action !=None:
            actions = list(ptype.listActions())
            ptype.deleteActions([actions.index(a) for a in actions if a.getId()=='seo_properties'])

return state.set(portal_status_message = 'Search Engine Optimizer updated.')
