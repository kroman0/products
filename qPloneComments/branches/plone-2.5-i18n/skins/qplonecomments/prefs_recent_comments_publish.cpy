## Script (Python) "prefs_recent_comments_publish"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

from Products.CMFCore.utils import getToolByName
from Products.qPloneComments.utils import publishDiscussion, send_email

request = context.REQUEST

comment_ids = request.get('ids')
portal_catalog = getToolByName(context, "portal_catalog")

for comment_id in comment_ids:
    comment = portal_catalog(id=comment_id,portal_type='Discussion Item')[0].getObject()    
    publishDiscussion(comment)
    send_notification_message = send_email(comment, container, state="published")

return state.set(portal_status_message='Comment(s) published.')

