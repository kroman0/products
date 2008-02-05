"""
    Tests for patched 'portal_atct'
"""

__docformat__ = 'restructuredtext'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))



from Testing import ZopeTestCase
ZopeTestCase.installProduct('qTopic')
from Products.ATContentTypes.tests import atcttestcase


from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.ATContentTypes.config import TOOLNAME
from Products.ATContentTypes.interfaces import IATCTTopicsTool
from Interface.Verify import verifyObject
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.interfaces import IATCTTool
from Products.ZCatalog.ZCatalog import manage_addZCatalog

# z3 imports
try:
    from Products.ATContentTypes.interface import IATCTTopicsTool as Z3IATCTTopicsTool
    from zope.interface.verify import verifyObject as Z3verifyObject
    z3_support = True
except ImportError:
    z3_support = False

tool_config = zconf.atct_tool.topic_tool


tests = []
index_def = {'index'        : 'end',
             'friendlyName' : 'End Date For Test',
             'description'  : 'This is an end Date',
             'criteria'     : ['ATDateCriteria','ATDateRangeCriteria']
            }
meta_def =  {'metadata'     : 'ModificationDate',
             'friendlyName' : 'Modification Date For Test',
             'description'  : ''
            }

conf_index_def = [i for i in tool_config.indexes if i.name == index_def['index']][0]
conf_meta_def = [m for m in tool_config.metadata if m.name == meta_def['metadata']][0]
CATALOG_NAME = 'test_catalog'
class TestTool(atcttestcase.ATCTSiteTestCase):

    def afterSetUp(self):
        self.tool = self.portal.portal_atct
        manage_addZCatalog(self.portal, id = CATALOG_NAME, title = 'Test catalog')
        self.cat = self.portal[CATALOG_NAME]
        self.cat.addIndex('end', 'DateIndex')
        self.cat.manage_addColumn(meta_def['metadata'])

    def test_interface(self):
        self.failUnless(IATCTTopicsTool.isImplementedBy(self.tool))
        self.failUnless(verifyObject(IATCTTopicsTool, self.tool))
    
 
    #Index tests
    def test_add_index(self):
        t = self.tool

        t.addIndex(enabled = True, catalog_name=CATALOG_NAME, **index_def)
        index = t.getIndex(index_def['index'], catalog_name=CATALOG_NAME)
        self.failUnlessEqual(index.index, index_def['index'])
        self.failUnlessEqual(index.friendlyName, index_def['friendlyName'])
        self.failUnlessEqual(index.description, index_def['description'])
        #Only need to test truth not actual value
        self.failUnless(index.enabled)
        self.failUnlessEqual(index.criteria, tuple(index_def['criteria']))

        self.failUnless(index in t.getEnabledIndexes(catalog_name=CATALOG_NAME))
        self.failUnless(index_def['index'] in [a[0] for a in t.getEnabledFields(catalog_name=CATALOG_NAME)])
        self.failUnless(index_def['index'] in t.getIndexDisplay(True, catalog_name=CATALOG_NAME).keys())
        self.failUnless(index_def['friendlyName'] in t.getIndexDisplay(True, catalog_name=CATALOG_NAME).values())
        self.failUnless(index_def['index'] in t.getIndexes(1))

    def test_disable_index(self):
        t = self.tool
        t.addIndex(enabled = False, catalog_name=CATALOG_NAME, **index_def)
        index = t.getIndex(index_def['index'], catalog_name=CATALOG_NAME)
        self.failUnlessEqual(index.index, index_def['index'])
        self.failUnlessEqual(index.friendlyName, index_def['friendlyName'])
        self.failUnlessEqual(index.description, index_def['description'])
        #Only need to test truth not actual value
        self.failIf(index.enabled)
        self.failUnlessEqual(index.criteria, tuple(index_def['criteria']))

        self.failIf(index in t.getEnabledIndexes(catalog_name=CATALOG_NAME))
        self.failIf(index_def['index'] in [a[0] for a in t.getEnabledFields(catalog_name=CATALOG_NAME)])
        self.failIf(index_def['index'] in t.getIndexes(1,catalog_name=CATALOG_NAME))
        self.failIf(index_def['index'] in t.getIndexDisplay(True, catalog_name=CATALOG_NAME).keys())
        self.failUnless(index_def['friendlyName'] not in t.getIndexDisplay(True, catalog_name=CATALOG_NAME).values())
        #Make sure it's still in the un-limited list
        self.failUnless(index_def['index'] in t.getIndexDisplay(False, catalog_name=CATALOG_NAME).keys())
        self.failUnless(index_def['friendlyName'] in t.getIndexDisplay(False, catalog_name=CATALOG_NAME).values())
        self.failUnless(index_def['index'] in t.getIndexes(catalog_name=CATALOG_NAME))

    def test_add_bogus_index(self):
        """An metdatum that's not in the catalog should be deleted automatically
           on any call to one of the index list methods."""
        t = self.tool
        t.addIndex('bogosity', enabled = True, catalog_name=CATALOG_NAME)
        error = False
        #The methods getEnabledFields, getEnabledIndexes, getIndexes,
        #getIndexDisplay, and getIndex all automatically restore fields
        #from the catalog

        try:
            t.getIndex('bogosity', catalog_name=CATALOG_NAME)
        except AttributeError:
            error = True
        self.failUnless(error)

        #Add
        t.addIndex('bogosity', enabled = True, catalog_name=CATALOG_NAME)
        self.failIf('bogosity' in [a[0] for a in t.getEnabledFields(catalog_name=CATALOG_NAME)])
        #Add
        t.addIndex('bogosity', enabled = True, catalog_name=CATALOG_NAME)
        self.failIf('bogosity' in t.getIndexDisplay(True, catalog_name=CATALOG_NAME).keys())
        #Add
        t.addIndex('bogosity', enabled = True, catalog_name=CATALOG_NAME)
        self.failIf('bogosity' in t.getIndexes(1, catalog_name=CATALOG_NAME))
        #Add
        t.addIndex('bogosity', enabled = True, catalog_name=CATALOG_NAME)
        self.failIf('bogosity' in [i.index for i in t.getEnabledIndexes(catalog_name=CATALOG_NAME)])

    def test_remove_index(self):
        t = self.tool
        t.addIndex(catalog_name=CATALOG_NAME, **index_def)
        t.removeIndex(index_def['index'], catalog_name=CATALOG_NAME)
        error = None
        try:
            index = t.topic_indexes[CATALOG_NAME][index_def['index']]
        except KeyError:
            error = True
        self.failUnless(error)
        #Should be restored automatically by getIndex and friends
        error = None
        try:
            index = t.getIndex(index_def['index'], catalog_name=CATALOG_NAME)
        except AttributeError:
            error = True
        self.failIf(error)
        #Make sure the FriendlyName is reset to default
        self.failUnlessEqual(index.friendlyName, getattr(conf_index_def,'friendlyName'))

    def test_update_index(self):
        """An index with no criteria set should set all available criteria,
           also changes made using updateIndex should not reset already set
           values"""
        t = self.tool
        t.addIndex(enabled = True, catalog_name=CATALOG_NAME, **index_def)
        t.updateIndex(index_def['index'], criteria = None,
                      description = 'New Description', catalog_name=CATALOG_NAME)
        index = t.getIndex(index_def['index'], catalog_name=CATALOG_NAME)
        self.failUnless(index.criteria)
        self.failUnless(index.criteria != index_def['criteria'])
        self.failUnless(index.description == 'New Description')
        self.failUnless(index.friendlyName == index_def['friendlyName'])
        self.failUnless(index.enabled)

    def test_all_indexes(self):
        """Ensure that the tool includes all indexes in the catalog"""
        t = self.tool
        cat = getToolByName(self.tool, CATALOG_NAME)
        indexes = [field for field in cat.indexes()]
        init_indexes = list(t.getIndexes(catalog_name=CATALOG_NAME))
        unique_indexes = [i for i in indexes if i not in init_indexes]
        unique_indexes = unique_indexes + [i for i in init_indexes if i not in indexes]
        self.failIf(unique_indexes)

    def test_change_catalog_index(self):
        """Make sure tool updates when indexes are added to or deleted from
           the catalog"""
        t = self.tool
        cat = getToolByName(self.tool, CATALOG_NAME)
        #add
        error = False
        cat.manage_addIndex('nonsense', 'FieldIndex')
        try:
            t.getIndex('nonsense', catalog_name=CATALOG_NAME)
        except AttributeError:
            error = True
        self.failIf(error)
        #remove
        error = False
        cat.delIndex('nonsense')
        try:
            t.getIndex('nonsense', catalog_name=CATALOG_NAME)
        except AttributeError:
            error = True
        self.failUnless(error)


    #Metadata tests
    def test_add_metadata(self):
        t = self.tool
        t.addMetadata(enabled = True, catalog_name=CATALOG_NAME,**meta_def)
        meta = t.getMetadata(meta_def['metadata'], catalog_name=CATALOG_NAME)
        self.failUnlessEqual(meta.index, meta_def['metadata'])
        self.failUnlessEqual(meta.friendlyName, meta_def['friendlyName'])
        self.failUnlessEqual(meta.description, meta_def['description'])
        #Only need to test truth not actual value
        self.failUnless(meta.enabled)

        self.failUnless(meta in t.getEnabledMetadata(catalog_name=CATALOG_NAME))
        self.failUnless(meta_def['metadata'] in t.getMetadataDisplay(True, catalog_name=CATALOG_NAME).keys())
        self.failUnless(meta_def['friendlyName'] in t.getMetadataDisplay(True, catalog_name=CATALOG_NAME).values())
        self.failUnless(meta_def['metadata'] in t.getAllMetadata(1, catalog_name=CATALOG_NAME))

    def test_disable_metadata(self):
        t = self.tool
        t.addMetadata(enabled = False, catalog_name=CATALOG_NAME, **meta_def)
        meta = t.getMetadata(meta_def['metadata'], catalog_name=CATALOG_NAME)
        self.failUnlessEqual(meta.index, meta_def['metadata'])
        self.failUnlessEqual(meta.friendlyName, meta_def['friendlyName'])
        self.failUnlessEqual(meta.description, meta_def['description'])
        #Only need to test truth not actual value
        self.failIf(meta.enabled)

        self.failUnless(meta not in t.getEnabledMetadata(catalog_name=CATALOG_NAME))
        self.failIf(meta_def['metadata'] in t.getAllMetadata(1, catalog_name=CATALOG_NAME))
        self.failIf(meta_def['metadata'] in t.getMetadataDisplay(True, catalog_name=CATALOG_NAME).keys())
        self.failIf(meta_def['friendlyName'] in t.getMetadataDisplay(True, catalog_name=CATALOG_NAME).values())
        #Make sure it's still in the un-limited list
        self.failUnless(meta_def['metadata'] in t.getMetadataDisplay(False, catalog_name=CATALOG_NAME).keys())
        self.failUnless(meta_def['friendlyName'] in t.getMetadataDisplay(False, catalog_name=CATALOG_NAME).values())
        self.failUnless(meta_def['metadata'] in t.getAllMetadata(catalog_name=CATALOG_NAME))

    def test_add_bogus_metadata(self):
        """An metdatum that's not in the catalog should be deleted automatically
           on any call to one of the index list methods"""
        t = self.tool
        t.addMetadata('bogosity', enabled = True, catalog_name=CATALOG_NAME)

        error = False
        #The methods getEnabledMetadata, getAllMetadata, getMetadataDisplay,
        #and getMetadata all automatically restore fields from the catalog
        try:
            t.getMetadata('bogosity', catalog_name=CATALOG_NAME)
        except AttributeError:
            error = True
        self.assert_(error)

        #Add
        t.addMetadata('bogosity', enabled = True, catalog_name=CATALOG_NAME)
        self.failIf('bogosity' in t.getMetadataDisplay(True, catalog_name=CATALOG_NAME).keys())
        #Add
        t.addMetadata('bogosity', enabled = True, catalog_name=CATALOG_NAME)
        self.failIf('bogosity' in t.getAllMetadata(1, catalog_name=CATALOG_NAME))
        #Add
        t.addMetadata('bogosity', enabled = True, catalog_name=CATALOG_NAME)
        self.failIf('bogosity' in [i.index for i in t.getEnabledMetadata(catalog_name=CATALOG_NAME)])

    def test_remove_metadata(self):
        t = self.tool
        t.addMetadata(catalog_name=CATALOG_NAME, **meta_def)
        t.removeMetadata(meta_def['metadata'], catalog_name=CATALOG_NAME)
        error = None
        try:
            meta = t.topic_metadata[CATALOG_NAME][meta_def['metadata']]
        except KeyError:
            error = True
        self.failUnless(error)
        #Should be restored automatically by getMetadata and friends
        error = None
        try:
            meta = t.getMetadata(meta_def['metadata'], catalog_name=CATALOG_NAME)
        except AttributeError:
            error = True
        self.failIf(error)
        #Make sure the FriendlyName is reset to default
        self.failUnlessEqual(meta.friendlyName, getattr(conf_meta_def,'friendlyName'))

    def test_update_metadata(self):
        """Changes made using updateMetadata should not reset already set
           values"""
        t = self.tool
        t.addMetadata(enabled = True, catalog_name=CATALOG_NAME, **meta_def)
        t.updateMetadata(meta_def['metadata'], friendlyName = 'New Name', catalog_name=CATALOG_NAME)
        meta = t.getMetadata(meta_def['metadata'], catalog_name=CATALOG_NAME)
        self.failUnless(meta.friendlyName == 'New Name')
        self.failUnless(meta.enabled)

    def test_all_metadata(self):
        """Ensure that the tool includes all metadata in the catalog"""
        t = self.tool
        cat = getToolByName(self.tool, CATALOG_NAME)
        metadata = [field for field in cat.schema()]
        init_metadata = list(t.getAllMetadata(catalog_name=CATALOG_NAME))
        unique_metadata = [i for i in metadata if i not in init_metadata]
        unique_metadata = unique_metadata + [i for i in init_metadata if i not in metadata]
        self.failIf(unique_metadata)

    def test_change_catalog_schema(self):
        """Make sure tool updates when columns are added to or deleted from
           the catalog"""
        t = self.tool
        cat = getToolByName(self.tool, CATALOG_NAME)
        #add
        error = False
        cat.manage_addColumn('nonsense')
        try:
            t.getMetadata('nonsense', catalog_name=CATALOG_NAME)
        except AttributeError:
            error = True
        self.failIf(error)
        #remove
        error = False
        cat.delColumn('nonsense')
        try:
            t.getMetadata('nonsense',catalog_name=CATALOG_NAME)
        except AttributeError:
            error = True
        self.assert_(error)
    
    if z3_support:
        def test_Z3interface(self):
            iface = Z3IATCTTopicsTool
            self.failUnless(Z3verifyObject(iface,self.tool))

tests.append(TestTool)

if __name__ == '__main__':
    framework()
else:
    # While framework.py provides its own test_suite()
    # method the testrunner utility does not.
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        for test in tests:
            suite.addTest(unittest.makeSuite(test))
        return suite
