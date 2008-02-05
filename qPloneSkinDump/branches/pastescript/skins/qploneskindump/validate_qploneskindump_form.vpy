## Controller Python Script "validate_qploneskindump_form.vpy"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Validates qPloneSkinDump form
##

from Products.CMFCore.utils import getToolByName
from Products.qPloneSkinDump.qPloneSkinDump import isValidProductName, isValidDirName
errors = state.getErrors()

def update_errors(existent_errors, new_errors):
    for e_name, e_value in new_errors.items():
        if e_name in existent_errors.keys():
            existent_errors[e_name] = existent_errors[e_name] + e_value
        else:
            existent_errors[e_name] = e_value

# Check REQUIRED fields
REQUIRED_FIELDS = ['ZMISkinName', 'ZMIBaseSkinName', 'FSProductName', 'FSSkinDirectory']
theform = {}
for f in REQUIRED_FIELDS:
    fdata = context.REQUEST.get(f, None)
    if not fdata:
        update_errors(errors, {f:u'Field is required.'})
    theform[f]=fdata

if not( theform['FSProductName'] and isValidProductName(theform['FSProductName']) ):
    update_errors(errors, {'FSProductName': u"Not valid Product name - read help attentively."})

if not( theform['FSSkinDirectory'] and isValidDirName(theform['FSSkinDirectory']) ):
    update_errors(errors, {'FSSkinDirectory': u"Not valid Skin name - read help attentively."})

if errors:
    return state.set(status='failure', errors=errors, portal_status_message='Please correct the indicated errors.')

return state
