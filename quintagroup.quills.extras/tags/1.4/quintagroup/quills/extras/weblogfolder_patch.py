from zope.component.interface import interfaceToName
from quills.core.interfaces import IPossibleWeblogEntry
from quills.core.interfaces import IWeblogLocator
from quills.app.interfaces import IWeblogEnhancedConfiguration
from quills.app.weblogentrybrain import WeblogEntryCatalogBrain


def getEntries(self, maximum=None, offset=0, path=None):
    """See IWeblog.
    """
    catalog, portal = self._setCatalog()
    catalog._catalog.useBrains(WeblogEntryCatalogBrain)
    weblog = IWeblogLocator(self.context).find()
    if getattr(weblog, 'context', None):
        # `weblog' is presumably an adapter around the real content object.
        weblog = weblog.context
                                        
    weblog_config = IWeblogEnhancedConfiguration(weblog)
    path = path or '/'.join(self.context.getPhysicalPath())
    results = catalog(
        object_provides=interfaceToName(portal, IPossibleWeblogEntry),
        path={ 'query' : path,
               'level' : 0, },
        sort_on='effective',
        sort_order='reverse',
        review_state={ 'query'    : weblog_config.published_states,
                       'operator' : 'or'})
    return self._filter(results, maximum, offset)


from Products.QuillsEnabled.adapters.folder import Folder2Weblog


Folder2Weblog.getEntries = getEntries
