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
from Products.qPloneComments.utils import publishDiscussion

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

portal_status_message='Comment published.'

putils = getToolByName(context, 'plone_utils')
redirect_target = putils.getDiscussionThread(talkback)[0]
view = redirect_target.getTypeInfo().getActionById('view')
anchor = reply.getId()

transaction_note('Published discussion item')
target = '%s/%s?portal_status_message=%s#%s' % (redirect_target.absolute_url(), view, portal_status_message, anchor)

return context.REQUEST.RESPONSE.redirect(target)