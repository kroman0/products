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
from Products.qPloneComments.utils import publishDiscussion

# Publish discussion item
publishDiscussion(context)

transaction_note('Published discussion item')
target = '%s/%s' % (context.absolute_url(), context.getTypeInfo().getActionById('view') )

return context.REQUEST.RESPONSE.redirect(target)