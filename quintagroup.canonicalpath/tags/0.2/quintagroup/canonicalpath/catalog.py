from zope.component import queryAdapter
from Products.CMFPlone.CatalogTool import registerIndexableAttribute

from interfaces import ICanonicalPath


def canonical_path(obj, portal, **kwargs):
    """Return canonical_path property for the object.
    """
    cpath = queryAdapter(obj, interface=ICanonicalPath)
    if cpath:
        return cpath.canonical_path()
    return None

registerIndexableAttribute('canonical_path', canonical_path)
