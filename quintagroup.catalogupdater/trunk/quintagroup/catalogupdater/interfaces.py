from zope.interface import Interface

class ICatalogUpdater(Interface):

    def updateMetadata4All(catalog, column):
        """ Update only the column metadata in the catalog
            for all records
        """

