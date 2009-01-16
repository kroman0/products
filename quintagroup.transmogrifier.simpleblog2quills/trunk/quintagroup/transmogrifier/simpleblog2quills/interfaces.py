from zope.interface import Interface

class IBlog(Interface):
    """ Marker interface for SimpleBlog blog object.
    """

class IBlogEntry(Interface):
    """ Marker interface for SimpleBlog blog entry object.
    """

class IItemManipulator(Interface):
    """ Interface for adapters that are looked up in 'itemmanipulator' 
        pipeline section.
    """

    def __call__(item, **kw):
        """ Do something with a pipeline item and return it.
            kw - dictionary with extra arguments, for example some useful keys
                in item (pathkey, ...)
        """

class IExportItemManipulator(IItemManipulator):
    """ Exporting adapter.
    """

class IImportItemManipulator(IItemManipulator):
    """ Importing adapter
    """
