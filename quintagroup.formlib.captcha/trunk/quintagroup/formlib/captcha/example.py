from zope import interface, schema
from zope.formlib import form
from zope.publisher.browser import TestRequest
from zope.interface import Interface
from quintagroup.formlib.captcha import Captcha
from zope.schema import TextLine
      
# Define CaptchaFormlibForm form schema

class ICaptchaFormlibFormSchema(Interface):
    label = TextLine(title=u'Label')
    captcha = Captcha(title=u'Type the code')
      
# Create adapter for any object to ICaptchaFormlibFormSchema
# schema interface

class CaptchaFormlibFormAdapter(object):
    adapts(interface.Interface)
    interface.implements(ICaptchaFormlibFormSchema)
    label = u''
    captcha = None
      
# And at the last define the CaptchaFormlibForm form

class CaptchaFormlibForm(form.EditForm):
    form_fields = form.FormFields(IFoo)
