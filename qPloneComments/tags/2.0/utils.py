from Products.CMFCore.utils import getToolByName

# Get apropriate property from (propery_sheeet) configlet
def getProp(self, prop_name, marker=None):
    result = marker
    pp = getToolByName(self, 'portal_properties')
    config_ps = getattr(pp, 'qPloneComments', None)
    if config_ps:
        result =  getattr(config_ps, prop_name, marker)
    return result


# Send notification e-mail on Discussion_Reply 
# Possible values for state: ["approve", "published"]
def send_email(reply, context, state="approve"):
    # Check is notification active
    notify = False
    if state=="approve":
        notify = getProp(context, "enable_approve_notification", False)
    elif state=="published":
        notify = getProp(context, "enable_published_notification", False)
    if not notify:
        return 0

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
        creator_id = parent.Creator()
        if creator_id:
            mtool = getToolByName(context, 'portal_membership')
            creator = mtool.getMemberById(creator_id)
            if creator:
                to_address = creator.getProperty('email', None)
    elif state=="approve":
        to_address = getProp(context, "email_discussion_manager", None)

    # Combine and send email
    if to_address:
        if state=="published":
            template = getattr(context, 'published_comment_template')
        elif state=="approve":
            template = getattr(context, 'approve_comment_template')

        organization_name = getProp(context, "email_subject_prefix", "")
        message = template(obj=parent, mto=to_address,
                           mfrom=from_address, organization_name=organization_name)
        try:
            host = context.MailHost
            host.send( message )
        except:
            return 0
    return 1

        
def publishDiscussion(self):
    roles = ['Anonymous']
    self.review_state = "published"
    self.manage_permission('View', roles, acquire=1)
    self._p_changed = 1
    self.reindexObject()


def setAnonymCommenting(context, allow=False):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    if allow:
        portal.manage_permission('Reply to item', ['Anonymous','Manager','Member'], 1)
    else:
        portal.manage_permission('Reply to item', ['Manager','Member'], 1)

    