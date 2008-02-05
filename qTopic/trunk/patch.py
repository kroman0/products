from Products.ATContentTypes.tool.topic import ATTopicsTool

from Globals import InitializeClass
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.criteria import _criterionRegistry
from AccessControl import ClassSecurityInfo
import Persistence
from OFS.SimpleItem import SimpleItem
from ExtensionClass import Base
from Acquisition import aq_base

from Products.CMFCore.permissions import ManagePortal
from Products.ATContentTypes.interfaces import IATCTTopicsTool

from Products.Archetypes.public import DisplayList
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.ATContentTypes.config import TOOLNAME

from Products.ATContentTypes.tool.topic import TopicIndex
from Products.ATContentTypes.configuration import zconf
tool_config = zconf.atct_tool.topic_tool

def __init__(self):
        self.topic_indexes = {}
        self.topic_indexes[CatalogTool.id] = {}
        self.topic_metadata = {}
        self.topic_metadata[CatalogTool.id] = {}
        self.allowed_portal_types = []

def _initializeTopicTool(self):
    """Helper method to initialize the topic tool
    """
    metadata = getattr(aq_base(self), 'topic_metadata', None)
    #test if metadata is empty or non existant, if so reinit.
    if not metadata:
        self.topic_indexes = {}
        self.topic_indexes[CatalogTool.id] = {}
        self.topic_metadata = {}
        self.topic_metadata[CatalogTool.id] = {}
        self.allowed_portal_types = []
        self.createInitialIndexes()
        self.createInitialMetadata()
        catalog_name = CatalogTool.id
        for index in tool_config.indexes:
            fn = getattr(index,'friendlyName',None)
            desc = getattr(index,'description',None)
            enabled = getattr(index,'enabled',None)
            criteria = getattr(index,'criteria',None)
            self.updateIndex(index.name, fn, desc, enabled, criteria, catalog_name)
        for meta in tool_config.metadata:
            fn = getattr(meta,'friendlyName',None)
            desc = getattr(meta,'description',None)
            enabled = getattr(meta,'enabled',None)
            self.updateMetadata(meta.name, fn, desc, enabled, catalog_name)
        return True
    else:
        return False

def getCriteriaForIndex(self, index, as_dict=False, catalog_name=CatalogTool.id):
    """ Returns the valid criteria for a given index """
    catalog_tool = getToolByName(self, catalog_name)
    try:
         indexObj = catalog_tool.Indexes[index]
    except KeyError:
        return ()
    criteria = tuple(_criterionRegistry.criteriaByIndex(indexObj.meta_type))
    search_criteria = _criterionRegistry.listSearchTypes()
    if as_dict:
        criteria = [{'name': a, 'description': _criterionRegistry[a].shortDesc}
                            for a in criteria if a in search_criteria]
    else:
        criteria = [a for a in criteria if a in search_criteria]
    criteria.sort()
    return criteria



def addIndex(self, index, friendlyName='', description='', enabled=False, criteria=None, catalog_name=CatalogTool.id):
    """ Add a new index along with descriptive information to the index
        registry """

    if not self.topic_indexes.has_key(catalog_name):
        self.topic_indexes[catalog_name]={}

    if criteria is None: criteria = self.getCriteriaForIndex(index, catalog_name)
    if self.topic_indexes[catalog_name].has_key(index):
        objIndex = self.topic_indexes[catalog_name][index]
        objIndex.friendlyName=friendlyName
        objIndex.description=description
        objIndex.enabled=enabled
        objIndex.criteria=tuple(criteria)
    else:
        objIndex = TopicIndex(index, friendlyName, description, enabled, criteria)

    self.topic_indexes[catalog_name][index]=objIndex
    self._p_changed=1


def addMetadata(self, metadata, friendlyName='', description='', enabled=False, catalog_name=CatalogTool.id):
    """ Add a new metadata field along with descriptive information to the
        metadata registry """

    if not self.topic_metadata.has_key(catalog_name):
        self.topic_metadata[catalog_name]={}

    if self.topic_metadata[catalog_name].has_key(metadata):
        objMeta = self.topic_metadata[catalog_name][metadata]
        objMeta.friendlyName=friendlyName
        objMeta.description=description
        objMeta.enabled=enabled
    else:
        objMeta = TopicIndex(metadata, friendlyName, description, enabled)

    if not self.topic_metadata[catalog_name]:
        self.topic_metadata[catalog_name] = {}
    self.topic_metadata[catalog_name][metadata]=objMeta
    self._p_changed=1



def updateIndex(self, index, friendlyName=None, description=None, enabled=None, criteria=None, catalog_name=CatalogTool.id):
    """ Updates an existing index in the registry, unrecognized values are
        added """

    indexes = self.topic_indexes[catalog_name]
    if friendlyName == None:
        friendlyName = indexes[index].friendlyName
    if description == None:
        description = indexes[index].description
    if enabled == None:
        enabled = indexes[index].enabled
    if criteria == None:
        criteria = indexes[index].criteria
    self.addIndex(index, friendlyName, description, enabled, criteria, catalog_name)


def updateMetadata(self, metadata, friendlyName=None, description=None, enabled=None, catalog_name=CatalogTool.id):
    """ Updates an existing metadata field in the registry, unrecognized values are
        added """
    if not self.topic_metadata.has_key(catalog_name):
        self.topic_metadata[catalog_name]={}
    meta = self.topic_metadata[catalog_name]
    if friendlyName == None:
        friendlyName = meta[metadata].friendlyName
    if description == None:
        description = meta[metadata].description
    if enabled == None:
        enabled = meta[metadata].enabled
    self.addMetadata(metadata, friendlyName, description, enabled, catalog_name)



def removeIndex(self, index, catalog_name=CatalogTool.id):
    """ Removes an existing index from the registry """
    if not self.topic_indexes.has_key(catalog_name):
        self.topic_indexes[catalog_name]={}
    if self.topic_indexes[catalog_name].has_key(index):
        del self.topic_indexes[catalog_name][index]
        self._p_changed=1


def removeMetadata(self, metadata, catalog_name=CatalogTool.id):
    """ Removes an existing metadata field from the registry """
    m = metadata
    if self.topic_metadata[catalog_name].has_key(metadata):
        del self.topic_metadata[catalog_name][metadata]
        self._p_changed=1


def createInitialIndexes(self, catalog_name=CatalogTool.id):
    """ create indexes for all indexes in the catalog """
    indexes = self.listCatalogFields()

    if not self.topic_indexes.has_key(catalog_name):
        self.topic_indexes[catalog_name]={}

    for i in indexes:
        if not self.topic_indexes[catalog_name].has_key(i):
            enabled = False
            self.addIndex(i, friendlyName='', enabled=enabled, catalog_name=catalog_name)
    return True


def createInitialMetadata(self, catalog_name=CatalogTool.id):
    """ create metadata for all indexes in the catalog """
    metas = self.listCatalogMetadata(catalog_name)

    if not self.topic_metadata.has_key(catalog_name):
        self.topic_metadata[catalog_name]={}

    for i in metas:
        if not self.topic_metadata[catalog_name].has_key(i):
            enabled = False
            self.addMetadata(i, friendlyName='', enabled=enabled, catalog_name=catalog_name)
    return True



def updateIndexesFromCatalog(self, catalog_name=CatalogTool.id):
    """ check if there are new indexes or if indexes must be removed from
        the collection because they do no longer exist in the catalog """
    indexes = self.listCatalogFields(catalog_name)
    configured_indexes = {}
    for index in tool_config.indexes:
        configured_indexes[index.name]=(getattr(index,'friendlyName',None),
                                        getattr(index,'description',None),
                                        getattr(index,'enabled',None),
                                        getattr(index,'criteria',None))

    # first add new indexes
    if not self.topic_indexes.has_key(catalog_name):
        self.topic_indexes[catalog_name]={}
    for i in indexes:
        if not self.topic_indexes[catalog_name].has_key(i):
            enabled = False
            defaults = (configured_indexes.has_key(i) and configured_indexes[i]) or \
                        ('','',enabled,self.getCriteriaForIndex(i,True,catalog_name))
            self.addIndex(i, friendlyName=defaults[0],
                        description=defaults[1], enabled=defaults[2],
                        criteria=defaults[3], catalog_name=catalog_name)

    # now check the other way round
    keys = self.topic_indexes[catalog_name].keys()
    for k in keys:
        if k not in indexes:
            self.removeIndex(k, catalog_name)


def updateMetadataFromCatalog(self, catalog_name=CatalogTool.id):
    """ check if there are new metadata fields or if fields must be
        removed from the collection because they do no longer exist in the
        catalog """
    metas = self.listCatalogMetadata(catalog_name)
    configured_metadata = {}
    for meta in tool_config.metadata:
        configured_metadata[meta.name]=(getattr(meta,'friendlyName',None),
                                        getattr(meta,'description',None),
                                        getattr(meta,'enabled',None))

    # first add new indexes
    if not self.topic_metadata.has_key(catalog_name):
        self.topic_metadata[catalog_name]={}
    for i in metas:
        if not self.topic_metadata[catalog_name].has_key(i):
            enabled = False
            defaults = (configured_metadata.has_key(i) and
                                    configured_metadata[i]) or ('','',enabled)
            self.addMetadata(i, friendlyName=defaults[0],
                            description=defaults[1], enabled=defaults[2], catalog_name=catalog_name)

    # now check the other way round
    keys = self.topic_metadata[catalog_name].keys()
    for k in keys:
        if k not in metas:
            self.removeMetadata(k, catalog_name)


def listCatalogFields(self, catalog_name=CatalogTool.id):
    """ Return a list of fields from catalog_name. """
    pcatalog = getToolByName( self, catalog_name)
    available = pcatalog.indexes()
    val = [ field for field in available ]
    val.sort()
    return val


def listCatalogMetadata(self, catalog_name=CatalogTool.id):
    """ Return a list of columns from portal_catalog. """
    pcatalog = getToolByName(self, catalog_name)
    available = pcatalog.schema()
    val = [ field for field in available ]
    val.sort()
    return val


def getEnabledIndexes(self, catalog_name=CatalogTool.id):
    """ Returns all TopicIndex objects for enabled indexes """
    # first resync with the catalog
    self.updateIndexesFromCatalog(catalog_name)

    indexes = self.topic_indexes[catalog_name]
    results = [i for i in indexes.values() if i.enabled]

    return results

def getEnabledMetadata(self, catalog_name=CatalogTool.id):
    """ Returns all TopicIndex objects for enabled metadata """
    # first resync with the catalog
    self.updateMetadataFromCatalog(catalog_name)

    meta = self.topic_metadata[catalog_name]
    results = [i for i in meta.values() if i.enabled]

    return results


def getIndexDisplay(self, enabled=True, catalog_name=CatalogTool.id):
    """ Return DisplayList of Indexes and their friendly names """
    if enabled:
        index_names = self.getIndexes(True, catalog_name)
    else:
        index_names = self.getIndexes(False, catalog_name)
    index_dict = self.topic_indexes[catalog_name]
    indexes = [index_dict[i] for i in index_names]

    field_list=[(f.index, f.friendlyName or f.index) for f in indexes]

    return DisplayList(field_list)

def getMetadataDisplay(self, enabled=True, catalog_name=CatalogTool.id):
    """ Return DisplayList of Metadata and their friendly names """
    if enabled:
        meta_names = self.getAllMetadata(True, catalog_name)
    else:
        meta_names = self.getAllMetadata(False, catalog_name)
    meta_dict = self.topic_metadata[catalog_name]
    meta = [meta_dict[i] for i in meta_names]

    field_list=[(f.index, f.friendlyName or f.index) for f in meta]

    return DisplayList(field_list)


def getEnabledFields(self, catalog_name=CatalogTool.id):
    """ Returns a list of tuples containing the index name, friendly name,
        and description for each enabled index. """
    enabledIndexes = self.getEnabledIndexes(catalog_name)

    dec_fields = [(i.friendlyName.lower() or i.index.lower(), i.index, i.friendlyName or i.index, i.description) for i in enabledIndexes]

    dec_fields.sort()

    fields = [(a[1],a[2],a[3]) for a in dec_fields]

    return fields


def getFriendlyName(self, index, catalog_name=CatalogTool.id):
    """ Returns the friendly name for a given index name, or the given
        index if the firendlyname is empty or the index is not recognized
    """
    if not self.topic_indexes.has_key(catalog_name):
        self.topic_indexes[catalog_name]={}

    if self.topic_indexes[catalog_name].has_key(index):
        return self.getIndex(index, catalog_name).friendlyName or index
    else:
        return index


def getIndexes(self, enabledOnly=False, catalog_name=CatalogTool.id):
    """ Returns the full list of available indexes, optionally filtering
        out those that are not marked enabled """
    # first resync with the catalog
    if  enabledOnly:
        indexes_dec = [(i.index.lower(), i.index) for i in self.getEnabledIndexes(catalog_name)]
    else:
        self.updateIndexesFromCatalog(catalog_name)
        indexes_dec = [(i.lower(), i) for i in self.topic_indexes[catalog_name].keys()]

    indexes_dec.sort()
    indexes = [i[1] for i in indexes_dec]
    return indexes

def getAllMetadata(self, enabledOnly=False, catalog_name=CatalogTool.id):
    """ Returns the full list of available metadata fields, optionally
        filtering out those that are not marked enabled """
    # first resync with the catalog
    self.updateMetadataFromCatalog(catalog_name)
    if enabledOnly:
        meta_dec = [(i.index.lower(), i.index) for i in self.getEnabledMetadata(catalog_name)]
    else:
        meta_dec = [(i.lower(), i) for i in self.topic_metadata[catalog_name].keys()]
    meta_dec.sort()
    metadata = [i[1] for i in meta_dec]
    return metadata


def getIndex(self, index, catalog_name=CatalogTool.id):
    """ Returns the TopicIndex object for a given index name """

    self.updateIndexesFromCatalog(catalog_name)
    if self.topic_indexes[catalog_name].has_key(index):
        return self.topic_indexes[catalog_name][index]
    else:
        raise AttributeError('Index ' + str(index) + ' not found')

def getMetadata(self, metadata, catalog_name=CatalogTool.id):
    """ Returns the TopicIndex object for a given metadata name """

    self.updateMetadataFromCatalog(catalog_name)
    if self.topic_metadata[catalog_name].has_key(metadata):
        return self.topic_metadata[catalog_name][metadata]
    else:
        raise AttributeError('Metadata ' + str(metadata) + ' not found')

def manage_saveTopicSetup(self, REQUEST=None):
    """ Set indexes and metadata from form """
    if REQUEST==None:
        return  'Nothing saved.'

    catalog_name=REQUEST.get('catalog', CatalogTool.id)

    data = REQUEST.get('index', [])
    for index in data:
        enabled = index.has_key('enabled')
        criteria = index.get('criteria', ())
        self.updateIndex(index['index'], index['friendlyName'], index['description'], enabled, criteria, catalog_name)

    meta = REQUEST.get('metadata', [])
    for metadata in meta:
        enabled = metadata.has_key('enabled')
        self.updateMetadata(metadata['index'], metadata['friendlyName'], metadata['description'], enabled, catalog_name)

    return 1

def clearIndexes(self, catalog_name=None):
    if not catalog_name:
        self.topic_indexes={}
        self.topic_metadata={}
        self.topic_indexes[CatalogTool.id] = {}
        self.topic_metadata[CatalogTool.id] = {}
    else:
        self.topic_indexes[catalog_name] = {}
        self.topic_metadata[catalog_name] = {}

ATTopicsTool.clearIndexes = clearIndexes
ATTopicsTool.old__init__ = ATTopicsTool.__init__
ATTopicsTool.__init__ = __init__
ATTopicsTool.old_initializeTopicTool = ATTopicsTool._initializeTopicTool
ATTopicsTool._initializeTopicTool = _initializeTopicTool
ATTopicsTool.old_getCriteriaForIndex = ATTopicsTool.getCriteriaForIndex
ATTopicsTool.getCriteriaForIndex = getCriteriaForIndex
ATTopicsTool.old_addIndex = ATTopicsTool.addIndex
ATTopicsTool.addIndex = addIndex
ATTopicsTool.old_addMetadata = ATTopicsTool.addMetadata
ATTopicsTool.addMetadata = addMetadata
ATTopicsTool.old_updateIndex = ATTopicsTool.updateIndex
ATTopicsTool.updateIndex = updateIndex
ATTopicsTool.old_updateMetadata = ATTopicsTool.updateMetadata
ATTopicsTool.updateMetadata = updateMetadata
ATTopicsTool.old_removeIndex = ATTopicsTool.removeIndex
ATTopicsTool.removeIndex = removeIndex
ATTopicsTool.old_removeMetadata = ATTopicsTool.removeMetadata
ATTopicsTool.removeMetadata = removeMetadata
ATTopicsTool.old_createInitialIndexes = ATTopicsTool.createInitialIndexes
ATTopicsTool.createInitialIndexes = createInitialIndexes
ATTopicsTool.old_createInitialMetadata = ATTopicsTool.createInitialMetadata
ATTopicsTool.createInitialMetadata = createInitialMetadata
ATTopicsTool.old_updateIndexesFromCatalog = ATTopicsTool.updateIndexesFromCatalog
ATTopicsTool.updateIndexesFromCatalog = updateIndexesFromCatalog
ATTopicsTool.old_updateMetadataFromCatalog = ATTopicsTool.updateMetadataFromCatalog
ATTopicsTool.updateMetadataFromCatalog = updateMetadataFromCatalog
ATTopicsTool.old_listCatalogFields = ATTopicsTool.listCatalogFields
ATTopicsTool.listCatalogFields = listCatalogFields
ATTopicsTool.old_listCatalogMetadata = ATTopicsTool.listCatalogMetadata
ATTopicsTool.listCatalogMetadata = listCatalogMetadata
ATTopicsTool.old_getEnabledIndexes = ATTopicsTool.getEnabledIndexes
ATTopicsTool.getEnabledIndexes = getEnabledIndexes
ATTopicsTool.old_getEnabledMetadata = ATTopicsTool.getEnabledMetadata
ATTopicsTool.getEnabledMetadata = getEnabledMetadata
ATTopicsTool.old_getIndexDisplay = ATTopicsTool.getIndexDisplay
ATTopicsTool.getIndexDisplay = getIndexDisplay
ATTopicsTool.old_getMetadataDisplay = ATTopicsTool.getMetadataDisplay
ATTopicsTool.getMetadataDisplay = getMetadataDisplay
ATTopicsTool.old_getEnabledFields = ATTopicsTool.getEnabledFields
ATTopicsTool.getEnabledFields = getEnabledFields
ATTopicsTool.old_getFriendlyName = ATTopicsTool.getFriendlyName
ATTopicsTool.getFriendlyName = getFriendlyName
ATTopicsTool.old_getIndexes = ATTopicsTool.getIndexes
ATTopicsTool.getIndexes = getIndexes
ATTopicsTool.old_getAllMetadata = ATTopicsTool.getAllMetadata
ATTopicsTool.getAllMetadata = getAllMetadata
ATTopicsTool.old_getIndex = ATTopicsTool.getIndex
ATTopicsTool.getIndex = getIndex
ATTopicsTool.old_getMetadata = ATTopicsTool.getMetadata
ATTopicsTool.getMetadata = getMetadata
ATTopicsTool.old_manage_saveTopicSetup= ATTopicsTool.manage_saveTopicSetup
ATTopicsTool.manage_saveTopicSetup= manage_saveTopicSetup