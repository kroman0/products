from zope.interface import Interface
from zope.formlib import form

from plone.app.users.browser.register import RegistrationForm

from quintagroup.plonecaptchas.browser.field import Captcha
from quintagroup.plonecaptchas import ProductMessageFactory as _

class ICaptchaSchema(Interface):
    captcha = Captcha(
        title=_(u'enter_word',
                default=u'Enter the word below'),
        description=_(u'label_help_captchas',
                      default=u"Enter the word below for registration. "))


class CustomRegistrationForm(RegistrationForm):
    """ For default registration form added captcha field.
    """

    @property
    def form_fields(self):
        defaultFields = super(CustomRegistrationForm, self).form_fields
        defaultFields += form.Fields(ICaptchaSchema)
        return defaultFields
