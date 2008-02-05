## Script (Python) "prefs_mapkeys_set"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= map_api_keys
##title=
##

from Products.CMFCore.utils import getToolByName
from Products.qPloneGoogleMaps.config import PROPERTY_SHEET, PROPERTY_FIELD

portal_props = getToolByName(context, 'portal_properties')

if not hasattr(portal_props, PROPERTY_SHEET):
    portal_props.addPropertySheet(PROPERTY_SHEET, 'Maps Properties')

property_sheet = getattr(portal_props, PROPERTY_SHEET)
property_sheet.manage_changeProperties(context.REQUEST)

return state.set(status='success', portal_status_message = '%s updated.' % PROPERTY_SHEET)