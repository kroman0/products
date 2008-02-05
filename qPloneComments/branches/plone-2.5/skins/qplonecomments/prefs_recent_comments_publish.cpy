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
from Products.qPloneComments.utils import publishDiscussion, manage_mails

request = context.REQUEST

comment_ids = request.get('ids', [])
portal_catalog = getToolByName(context, "portal_catalog")

for comment_id in comment_ids:
    comment = portal_catalog(id=comment_id,portal_type='Discussion Item')[0].getObject()
    publishDiscussion(comment)
    manage_mails(comment, container, action='publishing')

psm = comment_ids and 'Comment(s) published.' or 'Please select items to be processed.'
return state.set(portal_status_message=psm)
