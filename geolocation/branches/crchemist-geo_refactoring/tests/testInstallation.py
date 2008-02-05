
""" This module contains class that tests product's installation  procedure """

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestInstallation(PloneTestCase.PloneTestCase):
    """ Class for testing installation procedure """

    def afterSetUp(self):
        """ AfterSetUp features """
        self.qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.qi.installProduct(PRODUCT)

    def testLayerInstalling(self):
        """ Test skins layer installation """
        skinstool=getToolByName(self.portal, 'portal_skins')
        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map(string.strip, string.split(path, ','))
            self.failUnless(PRODUCT in path, 'geolocation layer not found in %s' % skin)

    def testLayerRemoving(self):
        """ Test skins layer uninstallation """
        self.qi.uninstallProducts([PRODUCT,])
        self.assertEqual(self.qi.isProductInstalled(PRODUCT), False,'geolocation is installed yet')
        skinstool=getToolByName(self.portal, 'portal_skins')
        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map(string.strip, string.split(path, ','))
            self.failIf(PRODUCT in path, 'geolocation layer found in %s after uninstallation' % skin)

    def testAddingGeoLocationAction(self):
        """ Test adding GEOLocation action to portal_types """
        ptypes = getToolByName(self.portal, 'portal_types')
        for tname in PORTAL_TYPES:
            tp = ptypes.getTypeInfo(tname)
            self.failUnless('edit_location' in [a.id for a in tp.listActions()],
                            "%s portal type haven't 'edit_location' action" % tname)

    def testRemovingGeoLocationAction(self):
        """ Test removing GEOLocation action from portal_types """
        self.qi.uninstallProducts([PRODUCT,])
        self.assertEqual(self.qi.isProductInstalled(PRODUCT), False,'geolocation is installed yet')
        ptypes = getToolByName(self.portal, 'portal_types')
        for tname in PORTAL_TYPES:
            tp = ptypes.getTypeInfo(tname)
            self.failIf('edit_location' in [a.id for a in tp.listActions()],
                            "%s portal type have 'edit_location' action" % tname)

    def testAddingCatalogIndex(self):
        """ Test adding index to portal_catalog tool """
        portal_catalog = getToolByName(self.portal, 'portal_catalog')
        self.failUnless(GEO_INDEX in portal_catalog.indexes(), 'Index not found in portal_catalog')

    def testAddingCatalogColumn(self):
        """ Test adding column to portal_catalog tool """
        portal_catalog = getToolByName(self.portal, 'portal_catalog')
        self.failUnless(GEO_INDEX in portal_catalog.schema(), 'Column not found in portal_catalog')

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    return suite

if __name__ == '__main__':
    framework()
