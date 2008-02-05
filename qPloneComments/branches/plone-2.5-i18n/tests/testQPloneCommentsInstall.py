#
# Test product's installation/uninstallation
#

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName

PRODUCT = 'qPloneComments'

PRODUCT_SKIN_NAME = "qplonecomments"
PROPERTY_SHEET = "qPloneComments"
CONFIGLET_ID = "prefs_comments_setup_form"

EMAIL_PID = "email_discussion_manager"
APPROVE_NOTIFICATION_PID = "enable_approve_notification"
PUBLISHED_NOTIFICATION_PID = "enable_published_notification"
MODERATION_PID = "enable_moderation"
ANONYMOUS_COMMENTING_PID = "enable_anonymous_commenting"

PERM_NAME = 'Moderate Discussion'
PloneTestCase.installProduct(PRODUCT)
PloneTestCase.setupPloneSite()


class TestInstallation(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

        self.qi = self.portal.portal_quickinstaller
        self.qi.installProduct(PRODUCT)

    def test_configlet_install(self):
        configTool = getToolByName(self.portal, 'portal_controlpanel', None)
        self.assert_(CONFIGLET_ID in [a.getId() for a in configTool.listActions()], 'Configlet not found')

    def test_skins_install(self):
        skinstool=getToolByName(self.portal, 'portal_skins') 

        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map( string.strip, string.split( path,',' ) )
            self.assert_(PRODUCT_SKIN_NAME in path, 'qPloneComments layer not found in %s' % skin)

    #def test_versionedskin_install(self):
    #    skinstool=getToolByName(self.portal, 'portal_skins')
    #    mtool = getToolByName(self.portal, 'portal_migration')
    #    plone_version = mtool.getFileSystemVersion()
    #
    #    for skin in skinstool.getSkinSelections():
    #        path = skinstool.getSkinPath(skin)
    #        path = map( string.strip, string.split( path,',' ) )
    #        self.assert_(PRODUCT+'/%s' % plone_version in path, 'qSEOptimizer versioned layer not found in %s' %skin)

    def test_propertysheet_install(self):
        portal_properties = getToolByName(self.portal, 'portal_properties', None)

        self.assert_(PROPERTY_SHEET in portal_properties.objectIds(), 'qPloneComments properies not found in portal_properties')

        property_ids = portal_properties[PROPERTY_SHEET].propertyIds()
        self.assert_(EMAIL_PID in property_ids, '%s propery not found in %s property' % (EMAIL_PID, PROPERTY_SHEET))
        self.assert_(APPROVE_NOTIFICATION_PID in property_ids, '%s propery not found in %s property' % (APPROVE_NOTIFICATION_PID, PROPERTY_SHEET))
        self.assert_(PUBLISHED_NOTIFICATION_PID in property_ids, '%s propery not found in %s property' % (PUBLISHED_NOTIFICATION_PID, PROPERTY_SHEET))
        self.assert_(MODERATION_PID in property_ids, '%s propery not found in %s property' % (MODERATION_PID, PROPERTY_SHEET))
        self.assert_(ANONYMOUS_COMMENTING_PID in property_ids, '%s propery not found in %s property' % (ANONYMOUS_COMMENTING_PID, PROPERTY_SHEET))


    def test_skins_uninstall(self):
        self.qi.uninstallProducts([PRODUCT])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT), True,'qPloneComments is already installed')
        skinstool=getToolByName(self.portal, 'portal_skins') 

        #self.assert_(not PRODUCT_SKIN_NAME in skinstool.objectIds(), '%s directory view found in portal_skins after uninstallation' % PRODUCT_SKIN_NAME)
        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map( string.strip, string.split( path,',' ) )
            self.assert_(not PRODUCT_SKIN_NAME in path, '%s layer found in %s after uninstallation' % (PRODUCT_SKIN_NAME, skin))

    #def test_versionedskin_uninstall(self):
    #    self.qi.uninstallProducts([PRODUCT])
    #    self.assertNotEqual(self.qi.isProductInstalled(PRODUCT), True,'qSEOptimizer is already installed')
    #    skinstool=getToolByName(self.portal, 'portal_skins')
    #    mtool = getToolByName(self.portal, 'portal_migration')
    #    plone_version = mtool.getFileSystemVersion()
    #
    #    for skin in skinstool.getSkinSelections():
    #        path = skinstool.getSkinPath(skin)
    #        path = map( string.strip, string.split( path,',' ) )
    #        self.assert_(not PRODUCT+'/%s' % plone_version in path, 'qSEOptimizer versioned layer found in %s after uninstallation' %skin)

    def test_configlet_uninstall(self):
        self.qi.uninstallProducts([PRODUCT])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT), True,'qPloneComments is already installed')
    
        configTool = getToolByName(self.portal, 'portal_controlpanel', None)
        self.assert_(not CONFIGLET_ID in [a.getId() for a in configTool.listActions()], 'Configlet found after uninstallation')

    def test_propertysheet_uninstall(self):
        self.qi.uninstallProducts([PRODUCT])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT), True,'qPloneComments is already installed')
        
        portal_properties = getToolByName(self.portal, 'portal_properties')
        self.assert_(not PROPERTY_SHEET in portal_properties.objectIds(), \
                     'qPloneComments property_sheet found in portal_properties after uninstallation')
    
    def test_permission_added(self):
	roles = [item['name'] for item in self.portal.rolesOfPermission(PERM_NAME)]
	self.assert_( roles != [], '%s not installed'%PERM_NAME)
        

TESTS = [TestInstallation]

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    return suite

if __name__ == '__main__':
    framework()

