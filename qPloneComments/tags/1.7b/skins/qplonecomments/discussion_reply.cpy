## Script (Python) "discussion_reply"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=subject,body_text,text_format='plain',username=None,password=None
from Products.PythonScripts.standard import url_quote_plus
from Products.qPloneComments.utils import send_email

req = context.REQUEST

if username or password:
    # The user username/password inputs on on the comment form were used,
    # which might happen when anonymous commenting is enabled. If they typed
    # something in to either of the inputs, we send them to 'logged_in'.
    # 'logged_in' will redirect them back to this script if authentication
    # succeeds with a query string which will post the message appropriately
    # and show them the result.  if 'logged_in' fails, the user will be
    # presented with the stock login failure page.  This all depends
    # heavily on cookiecrumbler, but I believe that is a Plone requirement.
    came_from = '%s?subject=%s&amp;body_text=%s' % (req['URL'], subject, body_text)
    came_from = url_quote_plus(came_from)
    portal_url = context.portal_url()

    return req.RESPONSE.redirect(
        '%s/logged_in?__ac_name=%s'
        '&amp;__ac_password=%s'
        '&amp;came_from=%s' % (portal_url,
                               url_quote_plus(username),
                               url_quote_plus(password),
                               came_from,
                               )
        )

# if (the user is already logged in) or (if anonymous commenting is enabled and
# they posted without typing a username or password into the form), we do
# the following

#########################################################
# Get discussion item (reply) author and creating reply #
isForAnonymous = context.isForAnonymous()
comment_creator = req.get('Creator', None)
if isForAnonymous and comment_creator:
    # Get entered anonymous name
    comment_creator = comment_creator
else:
    member = context.portal_membership.getAuthenticatedMember()
    # Get Member Full name.If not entered - get user login name
    comment_creator = member.getProperty('fullname')
    if not comment_creator:
        comment_creator = member.getUserName()

tb = context.talkback
id = tb.createReply(title=subject, text=body_text, Creator=comment_creator)
reply = tb.getReply(id)

#XXX THIS NEEDS TO GO AWAY!
portal_discussion=context.portal_discussion
if hasattr(portal_discussion.aq_explicit, 'cookReply'):
    portal_discussion.cookReply(reply, text_format='plain')

parent = tb.aq_parent

from Products.CMFPlone import transaction_note
transaction_note('Added comment to %s at %s' % (parent.title_or_id(), reply.absolute_url()))

target = '%s/%s' % (parent.absolute_url(), parent.getTypeInfo().getActionById('view'))

# Send notification e-mail
send_email(reply, context)

# Inform user about awaiting moderation
portal_status_message='Comment successfully added.'
ifModerate = context.ifModerate()
if ifModerate and reply:
    portal_status_message='Your comment awaits moderartion.'

return state.set(portal_status_message=portal_status_message)
