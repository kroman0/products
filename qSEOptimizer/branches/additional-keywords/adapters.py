from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.qSEOptimizer.interfaces import IKeywords


class AdditionalKeywords(object):
    implements(IKeywords)

    def __init__(self, context):
        self.context = context

    def listKeywords(self):
        portal_props = getToolByName(self.context, 'portal_properties')
        seo_props = getToolByName(portal_props, 'seo_properties')
        original = set(self.context.qSEO_Keywords())
        additional = set(seo_props.additional_keywords)
        text = set(self.context.SearchableText().split())
        keywords = list(additional.intersection(text).union(original))
        return ', '.join(keywords)
