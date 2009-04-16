from zope.interface import implements
from Products.CMFCore.utils import getToolByName

from quintagroup.portlet.cumulus.interfaces import ITagsRetriever

class GlobalTags(object):
    implements(ITagsRetriever)

    def __init__(self, context):
        self.context = context
        portal_properties = getToolByName(self.context, 'portal_properties')
        self.default_charset = portal_properties.site_properties.getProperty('default_charset', 'utf-8')

    def getTags(self, number=None):
        """ Entries of 'Categories' archetype field on content are assumed to be tags.
        """
        cat = getToolByName(self.context, 'portal_catalog')
        index = cat._catalog.getIndex('Subject')
        tags = []
        for name in index._index.keys():
            try:
                number_of_entries = len(index._index[name])
            except TypeError:
                number_of_entries = 1
            tags.append((name.decode(self.default_charset), number_of_entries, '#'))

        return tags
