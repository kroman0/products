from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from quintagroup.portlet.static import StaticStylishPortletMessageFactory as _

# Change the following default HTML class name with your own. Add more HTML classes to be available for you in Portlet style drop down menu 

PORTLET_CSS_STYLES = (
    (u"portletStaticClassOne", _(u"Class One")),
)

class PortletCSSVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [SimpleTerm(value, value, title) for value, title in PORTLET_CSS_STYLES]
        return SimpleVocabulary(items)

PortletCSSVocabulary = PortletCSSVocabulary()
