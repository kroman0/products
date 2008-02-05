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
# Discussion_Reply 
def send_email(reply, context):
    # Check is notification active
    notify = getProp(context, "Enable_Notification", False)
    if not notify:
        return
    # Get parent object
    parent = reply.inReplyTo()
    mt = parent.meta_type
    while mt == 'Discussion Item':
        try:
           parent = parent.inReplyTo()
           mt = parent.meta_type
        except:
           break

    # Get discussion manager's email
    admin_email = getProp(context, "Email_Discussion_Manager", None)

    # Set sending email to creator's or admin's one
    creator = parent.Creator()
    if creator:
        creator = context.portal_membership.getMemberById(creator)
        try:
            email = creator.getProperty('email',None)
        except:
            email = admin_email
        if not email:
            email = admin_email
    else:
        email = admin_email
    # Combine and send email
    if email:
        organization_name = getProp(context, "Email_Subject_Prefix", "")
        subject = "New comment added"
        bottom_sign = "Support Team."
        if organization_name:
            subject = "[%s] %s" % (organization_name, subject)
            bottom_sign = "%s %s" % (organization_name, bottom_sign)
            
        body = context.comment_template(obj=parent,
                                        mto=email,
                                        msubject=subject,
                                        mfrom=admin_email,
                                        mbsign=bottom_sign)
        mh = context.MailHost
        mh.send(body)  

        
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

    