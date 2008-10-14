from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from quintagroup.portlet.static import StaticStylishPortletMessageFactory as _

PORTLET_CSS_STYLES = (
    (u"portletStaticRed", _(u"Red")),
    (u"portletStaticLightGreen", _(u"Light Green")),
    (u"portletStaticOrange", _(u"Orange")),
    (u"portletStaticPurple", _(u"Purple")),
    (u"portletStaticBlue", _(u"Blue")),
    (u"portletStaticPale", _(u"Pale")),
    (u"portletStaticPaleBackground", _(u"Pale with Background")),
    (u"portletStaticBright", _(u"Bright")),
    (u"portletStaticBrightBackground", _(u"Bright with Background")),
)

class PortletCSSVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [SimpleTerm(value, value, title) for value, title in PORTLET_CSS_STYLES]
        return SimpleVocabulary(items)

PortletCSSVocabulary = PortletCSSVocabulary()
