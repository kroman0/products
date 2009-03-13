from zope.interface import implements
from zope.component import adapts

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IBaseContent

from interfaces import ICanonicalPath


class canonicalPathAdapter(object):
    """Adapts base content to canonical path.
    """
    adapts(IBaseContent)
    implements(ICanonicalPath)

    def __init__(self, context):
        self.context = context

    def canonical_path(self):
        purl = getToolByName(self.context,'portal_url')
        return '/'+'/'.join(purl.getRelativeContentPath(self.context))
