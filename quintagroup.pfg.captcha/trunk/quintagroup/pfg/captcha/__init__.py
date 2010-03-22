from zope.i18nmessageid import MessageFactory
ExamplePortletMessageFactory = MessageFactory('quintagroup.pfg.captcha')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
