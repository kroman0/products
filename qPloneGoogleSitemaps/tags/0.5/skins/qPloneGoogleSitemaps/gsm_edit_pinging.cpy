## Script (Python) "gsm_edit_pinging"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=transitions
##title=Configure Plone Google Sitemap
##

from Products.qPloneGoogleSitemaps.utils import setWorkflowTransitions
setWorkflowTransitions(context, transitions)

return state.set(portal_status_message = 'Plone Google Sitemap updated.')
