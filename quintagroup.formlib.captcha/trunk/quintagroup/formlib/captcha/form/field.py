from zope.interface import implements
from zope.schema import ASCIILine
from quintagroup.formlib.captcha.form.interfaces import ICaptcha


class Captcha(ASCIILine):
    implements(ICaptcha)
