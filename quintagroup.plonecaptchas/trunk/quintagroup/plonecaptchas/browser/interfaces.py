from zope.interface import Interface
from zope.schema.interfaces import IASCIILine
from plone.theme.interfaces import IDefaultPloneLayer

class ICaptchaView(Interface):
    """ Captcha generating and verifying view that is wrapper around
        captcha generation scripts located in skins folder.

        Use the view from a page to generate an image tag ('image_tag' method) 
        and to verify user input ('verify' method).
    """

    def image_tag():
        """Generate an image tag linking to a captcha"""

    def verify(input):
        """ Verify user input.
        """

class ICaptcha(IASCIILine):
    u"""A field for captcha validation"""


class IPloneChaptchaLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer bound to a Skin
       Selection in portal_skins.
    """
