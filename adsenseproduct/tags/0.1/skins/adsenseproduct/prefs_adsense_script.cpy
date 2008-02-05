## Controller Python Script "prefs_adsense_script"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=handles the adsense properties
##

request = context.REQUEST
portal_status_message="Changes not saved."

customer_id = request.get('customer_id', None)
if customer_id:
    from Products.CMFCore.utils import getToolByName
    pp = getToolByName(context, 'portal_properties')
    if pp and 'adsense_properties' in pp.objectIds() \
       and pp.adsense_properties.hasProperty('customer_id'):
        pp.adsense_properties.manage_changeProperties(customer_id=str(customer_id))
        portal_status_message="Changes saved."

return state.set(status="success", portal_status_message=portal_status_message)
