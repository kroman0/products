"""Catalog tool columns updater setup handlers.
"""
from zope.component import adapts
from zope.component import queryUtility

from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.interfaces import ISetupEnviron

from quintagroup.catalogupdater.interfaces import IUpdatableCatalog


class CatalogUpdaterXMLAdapter(XMLAdapterBase):
    """XML Catalog columns updater for CatalogTool.
    """

    adapts(IUpdatableCatalog, ISetupEnviron)

    _LOGGER_ID = 'catalogupdater'

    name = 'catalogupdater'

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        return ''

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        self._updateColumns(node)
        self._logger.info('Catalog columns updated.')


    def _updateColumns(self, node):
        columns = []
        for child in node.childNodes:
            if child.nodeName != 'column':
                continue
            col = str(child.getAttribute('value')).strip()
            columns.append(col)

        # Update columns in catalog
        if len(columns) > 0:

            catalog = self.context

            self._logger.info('Updating %s columns for %s Catalog.' % (
                columns, '/'.join(catalog.getPhysicalPaht())) )

            cu = queryUtility(ICatalogUpdater, name='catalog_updater')
            cu.updateMetadata4All(catalog, columns)


def updateCatalogColumns(context):
    """Update catalog columns with catalog_updater tool.
    """
    site = context.getSite()
    tool = getToolByName(site, 'portal_catalog')

    importObjects(tool, '', context)
