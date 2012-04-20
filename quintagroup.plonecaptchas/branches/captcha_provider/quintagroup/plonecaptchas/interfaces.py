from plone.theme.interfaces import IDefaultPloneLayer
from quintagroup.plonecaptchas.config import HAS_APP_DISCUSSION

if HAS_APP_DISCUSSION:
    from zope.publisher.interfaces.browser import IDefaultBrowserLayer
    from zope.interface import Interface, Attribute

    class IQGDiscussionCaptchas(IDefaultBrowserLayer):
        """ quintagroup.plonecaptchas browser layer interface for
            plone.app.discussion
        """

    class ICaptchaProvider(Interface):
        """ Captcha Provider
        """
        widget_factory = Attribute("Chaptcha widget factory")


class IQGPloneCaptchas(IDefaultPloneLayer):
    """ quintagroup.plonecaptchas browser layer interface """
