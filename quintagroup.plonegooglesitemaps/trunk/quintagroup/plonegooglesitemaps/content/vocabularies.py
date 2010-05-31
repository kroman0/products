from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from plone.app.vocabularies.types import BAD_TYPES

from Products.CMFCore.utils import getToolByName


class TypesWithInterfaceVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ttool = getToolByName(context, 'portal_types', None)
        if ttool is None:
            return None
        items = [ SimpleTerm(t, t, ttool[t].Title())
                  for t in ttool.listContentTypes()
                  if t not in BAD_TYPES ]
        return SimpleVocabulary(items)

TypesWithInterfaceVocabularyFactory = TypesWithInterfaceVocabulary()
