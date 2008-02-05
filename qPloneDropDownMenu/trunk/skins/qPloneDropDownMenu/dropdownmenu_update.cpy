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
request = container.REQUEST
RESPONSE =  request.RESPONSE

context.portal_dropdownmenu.regenerateMenu()

return state.set(status='success', portal_status_message='DropDown Menu regenerated.')