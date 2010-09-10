from zope.schema import TextLine
from zope.component import adapts
from zope.interface import Interface, implements
from zope.formlib.form import EditForm, FormFields

from quintagroup.formlib.captcha import Captcha
      
# Define CaptchaFormlibForm form schema

class ICaptchaFormlibFormSchema(Interface):
    label = TextLine(title=u'Label')
    captcha = Captcha(title=u'Type the code')
      
# Create adapter for any object to ICaptchaFormlibFormSchema
# schema interface

class CaptchaFormlibFormAdapter(object):
    implements(ICaptchaFormlibFormSchema)

    def __init__(self, context):
        self.context = context

    label = u''
    captcha = None
      
# And at the last define the CaptchaFormlibForm form

class CaptchaFormlibForm(EditForm):

    form_fields = FormFields(ICaptchaFormlibFormSchema)
