## Script (Python) "discussion_publish_comment"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=None
##title=
##
from Products.CMFPlone.utils import transaction_note
from Products.CMFCore.utils import getToolByName
from Products.qPloneComments.utils import publishDiscussion
from Products.qPloneComments.utils import manage_mails
from Products.CMFPlone import MessageFactory
qpcMF = MessageFactory('plonecomments')

if obj is None:
    obj = context

parent = obj.inReplyTo()
if parent is not None:
    dtool = getToolByName(context, 'portal_discussion')
    talkback = dtool.getDiscussionFor(parent)
else:
    talkback = parent = obj.aq_parent

reply = talkback.getReply(obj.getId())
publishDiscussion(reply)
manage_mails(reply, context, action='publishing')

putils = getToolByName(context, 'plone_utils')
redirect_target = putils.getDiscussionThread(talkback)[0]
view = redirect_target.getTypeInfo().getActionInfo('object/view')['url']
anchor = reply.getId()

transaction_note('Published discussion item')

context.plone_utils.addPortalMessage(qpcMF(u'Comment published.'))
target = '%s/%s#%s' % (redirect_target.absolute_url(), view, anchor)

return context.REQUEST.RESPONSE.redirect(target)
