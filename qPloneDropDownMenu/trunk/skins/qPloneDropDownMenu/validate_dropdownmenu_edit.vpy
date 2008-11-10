## Controlled Python Script "validate_dropdownmenu"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Validates a drop down menu edit_form contents
##

if state.getErrors():
    context.plone_utils.addPortalMessage('Please correct the indicated errors.')
    return state.set(status='failure')
return state
