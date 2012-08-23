from Acquisition import aq_inner
from OFS.SimpleItem import SimpleItem
from zope.component import adapts, getUtility
from zope.component.interfaces import ComponentLookupError
from zope.interface import Interface, implements
from zope.formlib import form
from zope import schema

from plone.app.contentrules.browser.formhelper import AddForm, EditForm 
from plone.contentrules.rule.interfaces import IRuleElementData, IExecutable

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import safe_unicode

from zope.sendmail.interfaces import IQueuedMailDelivery, IMailDelivery
import email.MIMEText
import email.Header
import re
attr_rexp = re.compile("\$\{item\.(\w+)\}")

class IMailAction(Interface):
    """Definition of the configuration available for a mail action
    """
    subject = schema.TextLine(title=_(u"Subject"),
            description=_(u"Subject of the message. ${title} replaced with object title"),
            required=True)

    groups = schema.TextLine(title=_(u"Recipients"),
            description=_("The group of users for whom you want to "
                   "send this message. To send it to different groups, just separate them with ,"),
            required=True)

    message = schema.Text(title=_(u"Message"),
            description=_(u"Type in here the message that you \
want to mail. Some defined content can be replaced: ${title} will be replaced \
by the title of the item. ${url} will be replaced by the URL of the item.\
${description} will be replaced by the description of the item.\
${item.<attribute>} will be replaced by the attribute of the item."),
            required=True)

class MailAction(SimpleItem):
    """
    The implementation of the action defined before
    """
    implements(IMailAction, IRuleElementData)

    subject = u''
    groups = u''
    message = u''

    element = 'quintagroup.actions.Mail'

    @property
    def summary(self):
        return _(u"Email report to ${groups}",
                 mapping=dict(groups=self.groups))


class MailActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IMailAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event


    def getEmailAddresses(self, groups):
        mtool = getToolByName(self.context, 'portal_membership')
        users_tool = getToolByName(self.context, 'acl_users')
        addresses = []
        for group_id in groups:
            group = users_tool.getGroupById(str(group_id))
            if group:
                members = group.getAllGroupMembers()
                addresses[:] = [(member.id, member.getProperty('email', ''))
                                for member in members
                                if member.getProperty('email', '') != '']

        return addresses


    def __call__(self):
        groups = self.element.groups.split(',')
        recipients = self.getEmailAddresses(groups) # list of email addresses

        mailer = getUtility(IMailDelivery, 'iw.mailer')

        obj = self.event.object
        event_title = safe_unicode(obj.Title())
        event_descr = safe_unicode(obj.Description())
        event_url = obj.absolute_url()

        urltool = getToolByName(aq_inner(self.context), "portal_url")
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')
        from_address = portal.getProperty('email_from_address')
        if not from_address:
            raise ValueError, 'You must enter an email in the portal properties'
        from_name = portal.getProperty('email_from_name')
        source = "%s <%s>" % (from_name, from_address)

        subject = self.element.subject.replace("${title}", event_title)
        
        for attr in attr_rexp.findall(subject):
            if getattr(obj, attr, None) is None:
                continue
            if callable(getattr(obj, attr)): 
                value = safe_unicode(getattr(obj, attr)())
            else: 
                value = safe_unicode(getattr(obj, attr))
            subject = subject.replace("${item.%s}" % attr, unicode(value))

        body = self.element.message.replace("${url}", event_url)
        body = body.replace("${title}", event_title).replace('${description}', event_descr)

        for attr in attr_rexp.findall(body):
            if getattr(obj, attr, None) is None:
                continue
            if callable(getattr(obj, attr)): 
                value = safe_unicode(getattr(obj, attr)())
            else: 
                value = safe_unicode(getattr(obj, attr))
            body = body.replace("${item.%s}" % attr, unicode(value))
        
        for userid, recipient in recipients:
            msgbody = body.replace('${userid}', userid)
            msg = email.MIMEText.MIMEText(msgbody.encode(email_charset), 'plain', email_charset)
            msg["From"] = source
            msg["Subject"] = email.Header.Header(subject, email_charset)
            msg['To'] = recipient

            mailer.send(source, [recipient], msg.as_string())
        return True

class MailAddForm(AddForm):
    """
    An add form for the mail action
    """
    form_fields = form.FormFields(IMailAction)
    label = _(u"Add Mail Action")
    description = _(u"A mail action can mail different recipient.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = MailAction()
        form.applyChanges(a, self.form_fields, data)
        return a

class MailEditForm(EditForm):
    """
    An edit form for the mail action
    """
    form_fields = form.FormFields(IMailAction)
    label = _(u"Edit Mail Action")
    description = _(u"A mail action can mail different recipient.")
    form_name = _(u"Configure element")

