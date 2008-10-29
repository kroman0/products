from zope.interface import Interface

class IExportDataCorrector(Interface):
    """ Inteface for components that do some data correction on export.
    """

    def __call__(data):
        """ Correct data given in 'data' argument and return it.
        """

class IImportDataCorrector(Interface):
    """ Inteface for components that do some data correction on import.
    """

    def __call__(data):
        """ Correct data given in 'data' argument and return it.
        """

# next is used in sitewalker.py

try:
    from Products.Archetypes.interfaces import IBaseFolder
except ImportError:
    class IBaseFolder(Interface):
        """Folderish base interface marker
        """

# next is used in propertymanager.py

try:
    from OFS.interfaces import IPropertyManager
except ImportError:
    class IPropertyManager(Interface):
        """ Marker interface for PropertyManager mixin.
        """

# next are used in adapters

try:
    from Products.ATContentTypes.interface import IATFile
except ImportError:
    class IATFile(Interface):
        """
        """

try:
    from Products.ATContentTypes.interface import IATImage
except ImportError:
    class IATImage(Interface):
        """
        """

try:
    from Products.ATContentTypes.interface import IATTopicCriterion
except ImportError:
    class IATTopicCriterion(Interface):
        """
        """
