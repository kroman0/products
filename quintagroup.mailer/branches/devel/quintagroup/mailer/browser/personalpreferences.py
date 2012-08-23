from plone.app.users.browser.personalpreferences import UserDataPanel
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from plone.app.users.userdataschema import IUserDataSchema
from Products.CMFDefault.formlib.widgets import FileUploadWidget

from zope import schema
from zope.formlib import form
from Products.CMFPlone import PloneMessageFactory as _

from quintagroup.mailer.config import GROUP_ID


class IQGMailerUserDataSchema(IUserDataSchema):
    alertssubscribed = schema.Bool(title=_(u'label_alertssubscribed_status', default=u'alertssubscribed'), description=u'', required=False)


class QGMailerUserDataPanel(UserDataPanel):
    def __init__(self, context, request):
        """ Load the UserDataSchema at view time.
        """
        super(QGMailerUserDataPanel, self).__init__(context, request)
        self.form_fields = form.FormFields(IQGMailerUserDataSchema)
        self.form_fields['portrait'].custom_widget = FileUploadWidget


class QGMailerUserDataConfiglet(QGMailerUserDataPanel):
    """ """


class QGMailerUserDataAdapter(UserDataPanelAdapter):

    def get_alertssubscribed(self):
        return self._getProperty('alertssubscribed')

    def set_alertssubscribed(self, value):
        group = self.context.acl_users.getGroup(GROUP_ID)
        member_id = self._getProperty('id')
        print member_id
        if value:
            group.addMember(member_id)
        else:
            group.removeMember(member_id)
        return self.context.setMemberProperties({'alertssubscribed': value})

    alertssubscribed = property(get_alertssubscribed, set_alertssubscribed)
