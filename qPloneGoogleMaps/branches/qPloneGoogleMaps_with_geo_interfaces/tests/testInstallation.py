
""" This module contains class that tests product's installation  procedure """

#PRODUCTS=('geolocation', 'qPloneGoogleMaps')

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestInstallation(PloneTestCase.PloneTestCase):
    """ Class for testing installation procedure """

    def afterSetUp(self):
        """ AfterSetUp features """
        self.properties = getToolByName(self.portal, 'portal_properties')
        self.qi = getToolByName(self.portal, 'portal_quickinstaller')
        #self.portal.changeSkin('Plone Default')
        self.qi.installProduct(PRODUCT)
        self._refreshSkinData()
        #self.loginAsPortalOwner()

    def testAddingPropertySheet(self):
        """ Test adding property sheet to portal_properties tool """
        self.failUnless(hasattr(self.properties.aq_base, PROPERTY_SHEET))

    def testAddingPropertyField(self):
        """ Test adding property field to portal_properties.maps_properties sheet """
        map_sheet = self.properties[PROPERTY_SHEET]
        self.failUnless(map_sheet.hasProperty(PROPERTY_FIELD) and map_sheet.getProperty(PROPERTY_FIELD)==MAP_API_KEYS)

    def testRemovingPropertySheet(self):
        """ Test removing property sheet from portal_properties tool """
        self.qi.uninstallProducts([PRODUCT,])
        self.assertEqual(self.qi.isProductInstalled(PRODUCT), False,'qPloneGoogleMaps is installed yet')
        self.failIf(hasattr(self.properties.aq_base, PROPERTY_SHEET),
                    "There should be no %s sheet in portal_properties tool." % PROPERTY_SHEET)

    def testConfigletInstalling(self):
        """ Test creating qPloneGoogleMaps configlet """
        configTool = getToolByName(self.portal, 'portal_controlpanel', None)
        self.failUnless(PRODUCT in [a.getId() for a in configTool.listActions()], 'Configlet not found')

    def testConfigletUninstall(self):
        """ Test removing qPloneGoogleMaps configlet """
        self.qi.uninstallProducts([PRODUCT,])
        self.assertEqual(self.qi.isProductInstalled(PRODUCT), False, 'qPloneGoogleMaps is installed yet')
        configTool = getToolByName(self.portal, 'portal_controlpanel', None)
        self.failIf(PRODUCT in [a.getId() for a in configTool.listActions()], 'Configlet found after uninstallation')

    def testAddingCatalogIndex(self):
        """ Test adding index to portal_catalog tool """
        portal_catalog = getToolByName(self.portal, 'portal_catalog')
        self.failUnless(GEO_INDEX in portal_catalog.indexes(), 'Index not found in portal_catalog')

    def testRemovingCatalogIndex(self):
        """ Test removing index from portal_catalog tool """
        self.qi.uninstallProducts([PRODUCT,])
        self.assertEqual(self.qi.isProductInstalled(PRODUCT), False, 'qPloneGoogleMaps is installed yet')
        portal_catalog = getToolByName(self.portal, 'portal_catalog')
        self.failIf(GEO_INDEX in portal_catalog.indexes(), 'Index should not be in in portal_catalog')

    def testAddingCatalogColumn(self):
        """ Test adding column to portal_catalog tool """
        portal_catalog = getToolByName(self.portal, 'portal_catalog')
        self.failUnless(GEO_INDEX in portal_catalog.schema(), 'Column not found in portal_catalog')

    def testRemovingCatalogColumn(self):
        """ Test removing column from portal_catalog tool """
        self.qi.uninstallProducts([PRODUCT,])
        self.assertEqual(self.qi.isProductInstalled(PRODUCT), False, 'qPloneGoogleMaps is installed yet')
        portal_catalog = getToolByName(self.portal, 'portal_catalog')
        self.failIf(GEO_INDEX in portal_catalog.schema(), 'Column should not be in in portal_catalog')

    def testInstallingContentTypes(self):
        """ Test installing content types """
        content_types = getToolByName(self.portal, 'portal_types').listTypeTitles().keys()
        for obj in NEW_PORTAL_TYPES:
            self.failUnless(obj in content_types, '%s content type not in portal_types tool' % obj)

    def testAddingToPortalFactory(self):
        """ Test adding content types to portal_factory tool """
        factory_types = getToolByName(self.portal, 'portal_factory').getFactoryTypes().keys()
        for obj in NEW_PORTAL_TYPES:
            self.failUnless(obj in factory_types,'%s content type not in factory_types tool' % obj)

    def testAddingFolderishMapView(self):
        """ Test adding map view template to folderish content types """
        portal_types = getToolByName(self.portal, 'portal_types', None)
        for tp in ['Folder', 'Large Plone Folder', 'Topic']:
            views = list(getattr(getattr(portal_types, tp, None), 'view_methods'))
            self.failUnless(TOPIC_VIEW in views, '%s should have a %s view template' % (tp, TOPIC_VIEW))

    def testRemovingFolderishMapView(self):
        """ Test removing map view template from folderish content types """
        self.qi.uninstallProducts([PRODUCT,])
        self.assertEqual(self.qi.isProductInstalled(PRODUCT), False, 'qPloneGoogleMaps is installed yet')
        portal_types = getToolByName(self.portal, 'portal_types', None)
        for tp in ['Folder', 'Large Plone Folder', 'Topic']:
            views = list(getattr(getattr(portal_types, tp, None), 'view_methods'))
            self.failIf(TOPIC_VIEW in views, '%s should not have a %s view template' % (tp, TOPIC_VIEW))

    def testAddingPortlets(self):
        """ Test adding portlets to right slot """
        right_slots = getattr(self.portal, 'right_slots', None)
        for slot in MAP_PORTLETS:
            self.failUnless(slot in right_slots, '%s not found in right slot' % slot)

    def testRemovingPortlets(self):
        """ Test removing portlets from right slot """
        self.qi.uninstallProducts([PRODUCT,])
        self.assertEqual(self.qi.isProductInstalled(PRODUCT), False, 'qPloneGoogleMaps is installed yet')
        right_slots = getattr(self.portal, 'right_slots', None)
        for slot in MAP_PORTLETS:
            self.failIf(slot in right_slots, '%s should not be in right slot' % slot)

    def testLayerInstalling(self):
        """ Test skins layer installation """
        skinstool=getToolByName(self.portal, 'portal_skins') 
        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map(string.strip, string.split(path, ','))
            self.failUnless(PRODUCT in path, 'qPloneGoogleMaps layer not found in %s' % skin)

    def testLayerRemoving(self):
        """ Test skins layer uninstallation """
        self.qi.uninstallProducts([PRODUCT,])
        self.assertEqual(self.qi.isProductInstalled(PRODUCT), False,'qPloneGoogleMaps is installed yet')
        skinstool=getToolByName(self.portal, 'portal_skins')
        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map(string.strip, string.split(path, ','))
            self.failIf(PRODUCT in path, 'qPloneGoogleMaps layer found in %s after uninstallation' % skin)

#tests.append(TestInstallation)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    return suite

if __name__ == '__main__':
    framework()
