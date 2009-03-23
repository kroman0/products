import unittest
import transaction
from Products.CMFCore.utils import getToolByName

from quintagroup.ploneformgen.readonlystringfield.tests.base import \
    ReadOnlyStringFieldTestCase


class TestErase(ReadOnlyStringFieldTestCase):
    
    def afterSetUp(self):
        self.loginAsPortalOwner()
        tool = getToolByName(self.portal, 'portal_quickinstaller')
        tool.installProduct('quintagroup.ploneformgen.readonlystringfield')
        tool.uninstallProducts(['quintagroup.ploneformgen.readonlystringfield'])
    
    def test_factoryTool(self):
        tool = getToolByName(self.portal, 'portal_factory')
        print tool._factory_types.keys()
        self.failIf('FormReadonlyStringField' in tool._factory_types.keys(),
            'FormReadonlyStringField type is still in portal_factory tool.')
    
    def test_typesTool(self):
        tool = getToolByName(self.portal, 'portal_types')
        self.failIf('FormReadonlyStringField' in tool.objectIds(),
            'FormReadonlyStringField type is still in portal_types tool.')
    
    def test_propertiesTool(self):
        tool = getToolByName(self.portal, 'portal_properties')
        navtree = tool.navtree_properties
        self.failIf('FormReadonlyStringField' in navtree.metaTypesNotToList,
            'FormReadonlyStringField is still in metaTypesNotToList property.')
        site = tool.site_properties
        self.failIf('FormReadonlyStringField' in site.types_not_searched,
            'FormReadonlyStringField is still in types_not_searched property.')
    
    def test_skinsTool(self):
        tool = getToolByName(self.portal, 'portal_skins')
        self.failIf('readonlystringfield' in tool.objectIds(),
            'There is still readonlystringfield folder in portal_skins.')
        for path_id, path in tool._getSelections().items():
            layers = [l.strip() for l in path.split(',')]
            self.failIf('readonlystringfield' in layers,
                'readonlystringfield layer is still in %s.' % path_id)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestErase))
    return suite
