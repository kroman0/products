from zope.formlib import form
from zope.interface import Interface
from plone.app.users.browser.register import AddUserForm
from plone.app.users.browser.register import RegistrationForm

from quintagroup.formlib.captcha import Captcha
from quintagroup.formlib.captcha import CaptchaWidget

from quintagroup.plonecaptchas import ProductMessageFactory as _

#from quintagroup.formlib.captcha.field import Captcha
class CaptchaSchema(Interface):
    captcha = Captcha(
        title=_(u'Type the code'),
        description=_(u'Type the code from the picture shown below.'))

class CaptchaRegistrationForm(RegistrationForm):
    """Registration form with captacha."""

    @property
    def form_fields(self):
        """Add captcha field to form_fields."""
        ffields = super(CaptchaRegistrationForm, self).form_fields
        if len(ffields):
            ffields = ffields + form.Fields(CaptchaSchema)
            ffields["captcha"].custom_widget = CaptchaWidget
        return ffields


class CaptchaAddUserForm(AddUserForm):
    """Add user form with captacha."""
