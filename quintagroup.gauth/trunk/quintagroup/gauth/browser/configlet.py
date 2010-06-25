from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from zope.schema import ASCII
#from zope.schema import TextLine
from zope.schema import Password
from zope.app.form.browser.textwidgets import ASCIIWidget

from zope.app.component.hooks import getSite

from plone.app.controlpanel.form import ControlPanelForm

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFDefault.formlib.schema import ProxyFieldProperty

from quintagroup.gauth import GAuthMessageFactory as _


# Configlet schemas
class IGAuthConfigletSchema(Interface):

    gauth_email = ASCII(
        title=_(u"Google Authentication email"),
        default=None,
        required=True)

    gauth_pass = Password(
        title=_(u'Google Authentication password'),
        default=None,
        required=True)

class GAuthConfigletAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IGAuthConfigletSchema)

    def __init__(self, context):
        super(GAuthConfigletAdapter, self).__init__(context)
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = pprop.gauth_properties

    gauth_email = ProxyFieldProperty(IGAuthConfigletSchema['gauth_email'])
    gauth_pass = ProxyFieldProperty(IGAuthConfigletSchema['gauth_pass'])


class GAuthConfiglet(ControlPanelForm):

    form_fields = form.FormFields(IGAuthConfigletSchema)
    form_fields['gauth_email'].custom_widget = ASCIIWidget
    label = _("Google Authentication settings")
    form_name = _("")
    description = _("")
