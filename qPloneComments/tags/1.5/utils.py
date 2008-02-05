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


# Checking is discussion item published
def isPublished(self):
    roles = self.permission_settings()
    roles = [r for r in roles if r['name']=='View']    

    if roles[0]['acquire']=='CHECKED':
       return 1
    return 0


# Send notification e-mail on 
# Discussion_Reply 
def send_email(reply, context):
    # Check is notification active
    notify = getProp(context, "Turning_on/off_notification", False)
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
    admin_email = getProp(context, "Email_of_discussion_manager", None)

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
        body = context.comment_template(obj=parent,
                                        mto=email,
                                        msubject="[Cornicen] New comment added",
                                        mfrom=admin_email)
        mh = context.MailHost
        mh.send(body)  
    
def publishDiscussion(self):
    roles = ['Anonymous']
    self.manage_permission('View', roles, acquire=1)


def setAnonymCommenting(context, allow=False):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    if allow:
        portal.manage_permission(ReplyToItem, ['Anonymous','Manager','Member'], 1)
    else:
        portal.manage_permission(ReplyToItem, ['Manager','Member'], 1)

    