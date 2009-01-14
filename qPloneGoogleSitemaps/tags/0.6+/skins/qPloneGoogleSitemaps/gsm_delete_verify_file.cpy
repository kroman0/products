## Script (Python) "create_verify_file"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Create file for verification
##

from Products.CMFCore.utils import getToolByName
props = getToolByName(context,'portal_properties').googlesitemap_properties

portal = getToolByName(context,'portal_url').getPortalObject()
try:
    if portal[props.verification_filename].CreatedBy == 'qPloneGoogleSitemaps':
        portal.manage_delObjects(props.verification_filename)
except:
    pass

props.manage_changeProperties(verification_filename = '')

return state.set(portal_status_message = 'Plone Google Sitemap updated.')
