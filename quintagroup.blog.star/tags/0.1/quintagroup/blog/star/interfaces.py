from zope import interface
from plone.theme.interfaces import IDefaultPloneLayer

class IQBlogStarLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """

class IQGBlogEntryRetriever(interface.Interface):

    def get_entries(year, month, **kw):
        """Retrieves all blog entries as catalog brains.
           with filtering by year, month and additional
           catalog indexes.
        """
