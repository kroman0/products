from zope.interface import Interface

class ICatalogUpdater(Interface):

    def updateMetadata4All(catalog, columns):
        """ Update metadata in the *catalog* for each column
            in the *columns* list for all records.

              * catalog - ZCatalog descendent catalog;
              * columns - list of metadata names, or
                          string with name of single
                          metadata, which must be updated.
        """

