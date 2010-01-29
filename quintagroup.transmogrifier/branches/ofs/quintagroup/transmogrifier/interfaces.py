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

class IFTIConstructor4MetaType(Interface):
    """FTI utility analogy for constuct instance for not CMF objects"""

    def _constructInstance(self, container, id, *args, **kw):
        """Build a bare instance of the appropriate type.
        Does not do any security checks.
        Returns the object without calling _finishConstruction().
        """

    def _finishConstruction(obj):
        """Finish the construction of a content object.
        Set its portal_type, insert it into the workflows.
        """
