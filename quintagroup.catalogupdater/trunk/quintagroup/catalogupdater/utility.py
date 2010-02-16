import logging, types
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

    def validate(self, cat, cols):
        # Validate catalog and column name
        AVAIL_COLTYPES = list(types.StringTypes) + [types.ListType, types.TupleType]

        _cat = getattr(cat, '_catalog', None)
        if _cat is None:
            raise AttributeError("%s - is not ZCatalog based catalog" % cat)

        if not type(cols) in AVAIL_COLTYPES:
            raise TypeError("'columns' parameter must be one of the following " \
                "types: %s" % AVAIL_COLTYPES)
        # Normalize columns
        if type(cols) in types.StringTypes:
            cols = [cols,]
        # Check is every column present in the catalog
        for col in cols:
            if not _cat.schema.has_key(col):
                raise AttributeError("'%s' - not presented column in %s catalog " % (col, cat))

        return _cat, cols

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


    def updateMetadata4All(self, catalog, columns):
        """ Look into appropriate method of ICatalogUpdate interface
        """

        _catalog, columns = self.validate(catalog, columns)

        portal = getToolByName(catalog, 'portal_url').getPortalObject()
        root = aq_parent(portal)
        
        data = _catalog.data
        schema = _catalog.schema
        paths = _catalog.paths

        # For each catalog record update metadata
        for rid, md in data.items():
            # get an object
            obj_uid = paths[rid]
            try:
                obj = root.unrestrictedTraverse(obj_uid)
                obj = self.getWrapedObject(obj, portal, catalog)
            except:
                LOG.error('updateMetadata4All could not resolve '
                          'an object from the uid %r.' % obj_uid)
                continue

            mdlist = list(md)
            for column in columns:
                # calculate the column value
                attr=getattr(obj, column, MV)
                if(attr is not MV and safe_callable(attr)): attr=attr()
                # Update metadata value
                indx = schema[column]
                mdlist[indx] = attr

            # Update catalog record
            data[rid] = tuple(mdlist)

