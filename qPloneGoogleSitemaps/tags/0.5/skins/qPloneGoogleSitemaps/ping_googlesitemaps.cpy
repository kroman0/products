## Script (Python) "ping_googlesitemaps.cpy"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Ping information to Google
##

from Products.CMFCore.utils import getToolByName
from Products.qPloneGoogleSitemaps.utils import ping_google

url = getToolByName(context, 'portal_url')()

portal_msg = "Google pinged. It will review your sitemap as soon as it will be able to."

try:
    ping_google(url)
except:
    portal_msg = "Cannot contact Google. Try again in a while."
    
return state.set(portal_status_message = portal_msg)