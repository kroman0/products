## Script (Python) "discussion_publish_comment"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=None
##title=
##
from Products.CMFPlone import transaction_note
from Products.CMFCore.utils import getToolByName
from Products.qPloneComments.utils import publishDiscussion, send_email

if obj is None:
    obj=context

parent = obj.inReplyTo()
if parent is not None:
    dtool = getToolByName(context, 'portal_discussion')
    talkback = dtool.getDiscussionFor(parent)
else:
    talkback = parent = obj.aq_parent

reply = talkback.getReply( obj.getId() )
publishDiscussion(reply)

send_notification_message = send_email(reply, container, state="published")

portal_status_message='Comment+successfully+published'

transaction_note('Published discussion item')
target = '%s/%s?portal_status_message=%s' % (context.absolute_url(), context.getTypeInfo().getActionById('view'), 
                                             portal_status_message)

return context.REQUEST.RESPONSE.redirect(target)