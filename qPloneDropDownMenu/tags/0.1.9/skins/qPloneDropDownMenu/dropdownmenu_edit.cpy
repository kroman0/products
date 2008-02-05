## Controller Python Script "dropdownmenu_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=menu=None, RESPONSE=None
##title=
##

REQUEST=context.REQUEST

properties = context.portal_properties.dropdownmenu_properties
properties.manage_editProperties(REQUEST)

return state.set(status='success', portal_status_message='DropDown Menu updated.')
