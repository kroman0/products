from zope.interface import Interface

#for compatibility with older plone versions 
try:
    from plone.indexer.decorator import indexer 
    IS_NEW = True
except:
    IS_NEW = False
    class IDummyInterface:pass
    class indexer:

         def __init__(self, *interfaces):
            self.interfaces = IDummyInterface,

         def __call__(self, callable):
             callable.__component_adapts__ = self.interfaces
             callable.__implemented__ = Interface
             return callable
    
@indexer(Interface)
def gsm_access(obj, **kwargs):
    """Return value for access tag for Google's News Sitemaps.
    """
    return obj.getProperty("gsm_access", "")

@indexer(Interface)
def gsm_genres(obj, **kwargs):
    """Return value for genres tag for Google's News Sitemaps.
    """
    return obj.getProperty("gsm_genres", "")


#for compatibility with older plone versions 
if not IS_NEW:
    from Products.CMFPlone.CatalogTool import registerIndexableAttribute
    map(registerIndexableAttribute, ('gsm_access', 'gsm_genres'),
                                    (gsm_access, gsm_genres))
