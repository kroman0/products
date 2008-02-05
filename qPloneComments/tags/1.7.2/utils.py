from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import ReplyToItem
from Products.qPloneComments.config import *

# Get apropriate property from (propery_sheeet) configlet
def getProp(self, prop_name, marker=None):
    result = marker
    pp = getToolByName(self, 'portal_properties')
    config_ps = getattr(pp, PROPERTY_SHEET, None)
    if config_ps:
        result =  getattr(config_ps, prop_name, marker)
    return result


# Send notification e-mail on 
# Possible values for state: ["approve", "published"]
def send_email(reply, context, state="approve"):
    # Check is notification active
    send_result = 0
    notify = False
    if state=="approve":
        notify = getProp(context, "Enable_Approve_Notification", False)
    elif state=="published":
        notify = getProp(context, "Enable_Published_Notification", False)
    if not notify:
        return send_result

    # Get parent object
    parent = reply.inReplyTo()
    mt = parent.meta_type
    while mt == 'Discussion Item':
        try:
           parent = parent.inReplyTo()
           mt = parent.meta_type
        except:
           break

    # Get portal admin e-mail
    portal = getToolByName(context, 'portal_url').getPortalObject()
    from_address = portal.getProperty('email_from_address')

    # Get email address based on state
    to_address = None
    if state=="published":
        creator = parent.Creator()
        if creator:
            mtool = getToolByName(context, 'portal_membership')
            creator = mtool.getMemberById(creator)
            to_address = creator.getProperty('email', None)
    elif state=="approve":
        to_address = getProp(context, "Email_Discussion_Manager", None)

    # Combine and send email
    if to_address:
        if state=="published":
            template = getattr(context, 'published_comment_template')
        elif state=="approve":
            template = getattr(context, 'approve_comment_template')

        organization_name = getProp(context, "Email_Subject_Prefix", "")
        message = template(obj=parent, mto=to_address,
                           mfrom=from_address, organization_name=organization_name)
        try:
            host = context.MailHost 
            host.send( message )
            send_result = 1
        except:
            send_result = 0
    return send_result

        
def publishDiscussion(self):
    roles = ['Anonymous']
    self.review_state = "published"
    self.manage_permission('View', roles, acquire=1)
    self._p_changed = 1


def setAnonymCommenting(context, allow=False):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    if allow:
        portal.manage_permission(ReplyToItem, ['Anonymous','Manager','Member'], 1)
    else:
        portal.manage_permission(ReplyToItem, ['Manager','Member'], 1)

    