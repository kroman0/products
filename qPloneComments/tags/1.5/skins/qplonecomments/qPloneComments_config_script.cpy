## Script (Python) "date_components_support"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.qPloneComments.config import PROPERTY_SHEET
from Products.qPloneComments.utils import setAnonymCommenting

form = context.REQUEST.form
pp = context.portal_properties
props_sheet = getattr(pp, PROPERTY_SHEET)
property_maps=[(m['id'], m['type']) for m in props_sheet.propertyMap() if not m['id']=='title']
request_ids = form.keys()

kw={}
for id,type in property_maps:
    if type == 'boolean':
        # For boolean type in REQUEST present ONLY CHECKED fields
        # PECULIARITY: when field uncheck - it disappear from the REQUEST
        if id in request_ids:
            kw[id] = True
        else:
            kw[id] = False

        # Switch anonymouse commenting
        if id == 'Turning_on/off_Anonymous_Commenting':
            allow = False
            if id in request_ids:
                allow = True
            setAnonymCommenting(context, allow)
    else:
        if id in request_ids:
            kw[id] = form[id]

props_sheet.manage_changeProperties(kw)

return state.set(portal_status_message='Document changes saved.')