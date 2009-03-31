## Controller Python Script "dropdownmenu_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=menu
##title=
##

from Products.CMFCore.utils import getToolByName

# some checks whether dropdown properties exist
pp = getToolByName(context, 'portal_properties')
if 'dropdownmenu_properties' not in pp.objectIds():
    context.plone_utils.addPortalMessage('Dropdown menu property sheet does not exist. Please, firstly regenerate menu before editing it.',
                                         type='error')
    return state.set(status='failure')


properties = pp.dropdownmenu_properties
if not properties.hasProperty('menu'):
    context.plone_utils.addPortalMessage('menu field does not exist in dropdown menu property sheet. Please, firstly regenerate menu before editing it.',
                                         type='error')
    return state.set(status='failure')

# do actual work
properties.manage_changeProperties(menu=menu)
context.plone_utils.addPortalMessage('DropDown Menu updated.')
return state.set(status='success')
