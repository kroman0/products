## Script (Python) "prefs_recent_comments_delete"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.CMFCore.utils import getToolByName
from Products.qPloneComments.utils import manage_mails
portal_discussion = getToolByName(context, "portal_discussion")
portal_catalog = getToolByName(context, "portal_catalog")

request = context.REQUEST
comment_ids = request.get('ids', [])

for comment_id in comment_ids:
    comment = portal_catalog(id=comment_id,portal_type='Discussion Item')[0].getObject()

    parent = comment.inReplyTo()
    if parent is not None:
        talkback = portal_discussion.getDiscussionFor(parent)
    else:
        talkback = parent = comment.aq_parent

    comment = portal_catalog(id=comment_id,portal_type='Discussion Item')[0].getObject()
    talkback.deleteReply(comment_id)
    manage_mails(comment, context, 'deleting')

psm = comment_ids and 'Comment(s) deleted.' or 'Please select items to be processed.'
return state.set(portal_status_message=psm)
