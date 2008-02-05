## Controller Python Script "validate_qploneskindump_generate.vpy"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Validates qPloneSkinDump generate form
##

from Products.CMFCore.utils import getToolByName
REQUEST = context.REQUEST

layer_name = REQUEST.get('Layer')
skin_name = REQUEST.get('Skin')
subfolder_name = REQUEST.get('Subfolder')

skins_tool = getToolByName(context, 'portal_skins')
errors = state.getErrors()

def update_errors(existent_errors, new_errors):
    for e_name, e_value in new_errors.items():
        if e_name in existent_errors.keys():
            existent_errors[e_name] = existent_errors[e_name] + e_value
        else:
            existent_errors[e_name] = e_value

if subfolder_name in skins_tool[layer_name].objectIds():
    update_errors(errors, {'Subfolder': u"Folder with this name already exists, please choose another name or "})

if errors:
    return state.set(status='failure', errors=errors, portal_status_message='Please correct the indicated error.')

return state
