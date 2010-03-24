from base import *

class TestInstallation(TestCaseNotInstalled):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.qi = getToolByName(self.portal, 'portal_quickinstaller', None)
        self.skins = getToolByName(self.portal, 'portal_skins', None)
        self.qi.installProduct(PRODUCT_NAME)

    def testSkinInstall(self):
        for skin in self.skins.getSkinSelections():
            path = self.skins.getSkinPath(skin)
            path = map(str.strip, path.split(','))
            for layer in LAYERS:
                self.assert_(layer.split('/')[0] in self.skins.objectIds(),
                    '%s directory view not found in portal_skins after installation' % layer)
                self.assert_(layer in path,
                    '%s layer not found in %s' % (PRODUCT_NAME, skin))

    def testSkinUninstall(self):
        self.qi.uninstallProducts([PRODUCT_NAME])
        assert not self.qi.isProductInstalled(PRODUCT_NAME)

        for skin in self.skins.getSkinSelections():
            path = self.skins.getSkinPath(skin)
            path = map(str.strip, path.split(','))
            for layer in LAYERS:
                self.assertTrue(not layer.split('/')[0] in self.skins.objectIds(),
                    '%s directory view found in portal_skins after uninstallation' % layer)
                self.assert_(not layer in path,
                    '%s layer found in %s skin after uninstallation' % (layer, skin))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestInstallation))
    return suite
