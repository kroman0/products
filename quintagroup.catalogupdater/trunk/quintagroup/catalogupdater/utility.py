import logging
from zope.interface import implements
from zope.component import queryMultiAdapter
from plone.indexer.interfaces import IIndexableObject

from Missing import MV
from Acquisition import aq_inner
from Acquisition import aq_parent

from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.Catalog import safe_callable
from Products.CMFPlone.CatalogTool import register_bbb_indexers
from Products.CMFPlone.CatalogTool import _old_IIndexableObjectWrapper

from quintagroup.catalogupdater.interfaces import ICatalogUpdater

LOG = logging.getLogger('quintagroup.catalogupdater')


class CatalogUpdaterUtility(object):

    implements(ICatalogUpdater)

    def validate(self, cat, col):
        # Validate catalog and column name
        _cat = getattr(cat, '_catalog', None)

        if _cat is None:
            raise AttributeError("%s - is not ZCatalog based catalog" % cat)

        if not _cat.schema.has_key(col):
            raise AttributeError("'%s' - not presented column in %s catalog " % (col, cat))

    def getWrapedObject(self, obj, portal, catalog):
       # Returned wrapped 'obj' object with IIndexable wrapper
       w = obj
       if not IIndexableObject.providedBy(obj):
            # BBB: Compatibility wrapper lookup. Should be removed in Plone 4.
            register_bbb_indexers()
            wrapper = queryMultiAdapter((obj, portal), _old_IIndexableObjectWrapper)
            if wrapper is not None:
                w = wrapper
            else:
                # This is the CMF 2.2 compatible approach, which should be used going forward
                wrapper = queryMultiAdapter((obj, catalog), IIndexableObject)
                if wrapper is not None:
                    w = wrapper
       return w


    def updateMetadata4All(self, catalog, column):
        """ Look into appropriate method of ICatalogUpdate interface
        """
        self.validate(catalog, column)

        _catalog = catalog._catalog
        portal = getToolByName(catalog, 'portal_url').getPortalObject()
        root = aq_parent(portal)
        
        data = _catalog.data
        schema = _catalog.schema
        indx = schema[column]
        paths = _catalog.paths

        # For each catalog record update metadata
        for rid, md in data.items():
            # get an object
            obj_uid = paths[rid]
            try:
                obj = root.unrestrictedTraverse(obj_uid)
                obj = self.getWrapedObject(obj, portal, catalog)
            except:
                LOG.error('update_metadata_column could not resolve '
                          'an object from the uid %r.' % obj_uid)
                continue

            # calculate the column value
            mdlist = list(md)
            attr=getattr(obj, column, MV)
            if(attr is not MV and safe_callable(attr)): attr=attr()

            # update metadata value
            mdlist[indx] = attr
            data[rid] = tuple(mdlist)

