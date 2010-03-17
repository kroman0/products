from zope.interface import Interface
from zope.component import queryAdapter
from plone.indexer.decorator import indexer

from interfaces import ICanonicalPath
from interfaces import ICanonicalLink

@indexer(Interface)
def canonical_path(obj, **kwargs):
    """Return canonical_path property for the object.
    """
    adapter = queryAdapter(obj, interface=ICanonicalPath)
    if adapter:
        return adapter.canonical_path
    return None

@indexer(Interface)
def canonical_link(obj, **kwargs):
    """Return canonical_link property for the object.
    """
    adapter = queryAdapter(obj, interface=ICanonicalLink)
    if adapter:
        return adapter.canonical_link
    return None
