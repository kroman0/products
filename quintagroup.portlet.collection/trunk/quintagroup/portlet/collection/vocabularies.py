from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from Products.CMFCore.utils import getToolByName

from quintagroup.portlet.collection import MessageFactory as _
from quintagroup.portlet.collection.utils import getStylesVocabulary

PORTLET_CSS_STYLES = (
     (u"class1", _(u"Class1")),
     (u"class2", _(u"Class2")),
)

PORTLET_ATTRIBUTES_TO_SHOW = (
     (u"Title", _(u"Title")),
     (u"Description", _(u"Description")),
)

class PortletCSSVocabulary(object):
    implements(IVocabularyFactory)


    def __call__(self, context):
        styles = getStylesVocabulary(context)
        if styles is None:
            styles = PORTLET_CSS_STYLES
        charset = self._charset(context)
        items = []
        for value, title in styles:
            if not isinstance(title, unicode):
                title = title.decode(charset)
            if not isinstance(value, unicode):
                value = value.decode(charset)
            items.append(SimpleTerm(value, value, _(title)))
        return SimpleVocabulary(items)

    def _charset(self, context):
        pp = getToolByName(context, 'portal_properties', None)
        if pp is not None:
            site_properties = getattr(pp, 'site_properties', None)
            if site_properties is not None:
                return site_properties.getProperty('default_charset', 'utf-8')
            return 'utf-8'

PortletCSSVocabulary = PortletCSSVocabulary()

class PortletAttributesVocabulary(object):
     implements(IVocabularyFactory)

     def __call__(self, context):
         items = [SimpleTerm(value, value, title) for value, title in PORTLET_ATTRIBUTES_TO_SHOW]
         return SimpleVocabulary(items)

PortletAttributesVocabulary = PortletAttributesVocabulary()

