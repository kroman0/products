## Script (Python) "dropdownmenu_update"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##

from Products.CMFCore.utils import getToolByName

getToolByName(context, 'portal_dropdownmenu').regenerateMenu()
context.plone_utils.addPortalMessage('DropDown Menu regenerated.')
return state.set(status='success')