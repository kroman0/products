## Script (Python) "gsm_edit_settings"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=states, portalTypes, blackout_list, reg_exp, urls
##title=Configure Plone Google Sitemap
##

from Products.CMFCore.utils import getToolByName
from Products.qPloneGoogleSitemaps.utils import setWorkflowTransitions
import Products.qPloneGoogleSitemaps.config as config

props = getToolByName(context,'portal_properties').googlesitemap_properties
props.manage_changeProperties( states=states, portalTypes=portalTypes,
                               blackout_list=blackout_list, reg_exp = reg_exp,
                               urls = urls)

return state.set(portal_status_message = 'Plone Google Sitemap updated.')
