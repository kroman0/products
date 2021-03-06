## Script (Python) "create_verify_file"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=verify_filename
##title=Create file for verification
##

from Products.CMFCore.utils import getToolByName
from Products.qPloneGoogleSitemaps.utils import BadRequestException
portal = getToolByName(context, 'portal_url').getPortalObject()
try:
    portal.manage_addFile(verify_filename,title='Verification File')
    portal[verify_filename].manage_addProperty('CreatedBy','qPloneGoogleSitemaps','string')
except BadRequestException:
    pass
props = getToolByName(context,'portal_properties').googlesitemap_properties
props.manage_changeProperties(verification_filename = verify_filename)


return state.set(portal_status_message = 'Plone Google Sitemap updated.')
