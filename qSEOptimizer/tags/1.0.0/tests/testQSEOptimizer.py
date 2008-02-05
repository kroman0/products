#
# Test installation script
#

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Products.CMFQuickInstallerTool.InstalledProduct import InstalledProduct

try:
    from Products.CMFCore.CMFCorePermissions import ManagePortal
except:
    from Products.CMFCore.permissions import ManagePortal

from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager
import re

from Products.qSEOptimizer.config import *

props = {'stop_words':STOP_WORDS, 'fields':FIELDS}

configlets = ({'id':'qSEOptimizer',
    'name':'Search Engine Optimizer',
    'action':'string:${portal_url}/prefs_qseo_setup_form',
    'condition':'',
    'category':'Products',
    'visible':1,
    'appId':'qSEOptimizer',
    'permission':ManagePortal},)

PRODUCT = 'qSEOptimizer'
qSEO_CONTENT = ['File','Document','News Item','BlogEntry']
qSEO_FOLDER  = []
qSEO_TYPES   = qSEO_CONTENT + qSEO_FOLDER

PloneTestCase.installProduct(PRODUCT)
PloneTestCase.setupPloneSite()


class TestInstallation(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.properties = getToolByName(self.portal, 'portal_properties')
        self.qi = self.portal.portal_quickinstaller
        self.qi.installProduct(PRODUCT)

    def testAddingPropertySheet(self):
        """ Test adding property sheet to portal_properties tool """
        self.failUnless(hasattr(self.properties.aq_base, PROPERTY_SHEET))

    def testAddingPropertyFields(self):
        """ Test adding property field to portal_properties.maps_properties sheet """
        map_sheet = self.properties[PROPERTY_SHEET]
        for key, value in props.items():
            self.failUnless(map_sheet.hasProperty(key) and list(map_sheet.getProperty(key)) == value)

    def test_configlet_install(self):
        configTool = getToolByName(self.portal, 'portal_controlpanel', None)
        self.assert_(PRODUCT in [a.getId() for a in configTool.listActions()], 'Configlet not found')

    def test_actions_install(self):
        portal_types = getToolByName(self.portal, 'portal_types')
        for ptype in portal_types.objectValues():
            try:
                #for Plone-2.5 and higher
                acts = filter(lambda x: x.id == 'seo_properties', ptype.listActions())
                action = acts and acts[0] or None
            except AttributeError:
                action = ptype.getActionById('seo_properties', default=None )

            if ptype.getId() in qSEO_TYPES:
                self.assert_(action, 'Action for %s not found' % ptype.getId())
            else:
                self.assert_(not action, 'Action found for %s' % ptype.getId())

    def test_skins_install(self):
        skinstool=getToolByName(self.portal, 'portal_skins') 

        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map( string.strip, string.split( path,',' ) )
            self.assert_(PRODUCT in path, 'qSEOptimizer layer not found in %s' %skin)

    def test_versionedskin_install(self):
        skinstool=getToolByName(self.portal, 'portal_skins')
        mtool = getToolByName(self.portal, 'portal_migration')
        plone_version = mtool.getFileSystemVersion()
        if plone_version < "3":
            for skin in skinstool.getSkinSelections():
                path = skinstool.getSkinPath(skin)
                path = map( string.strip, string.split( path,',' ) )
                self.assert_(PRODUCT+'/%s' % plone_version in path, 'qSEOptimizer versioned layer not found in %s' %skin)

    def test_actions_uninstall(self):
        self.qi.uninstallProducts([PRODUCT])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT), True,'qSEOptimizer is already installed')
        portal_types = getToolByName(self.portal, 'portal_types')
        for ptype in portal_types.objectValues():
            try:
                #for Plone-2.5 and higher
                acts = filter(lambda x: x.id == 'seo_properties', ptype.listActions())
                action = acts and acts[0] or None
            except AttributeError:
                action = ptype.getActionById('seo_properties', default=None )

            self.assert_(not action, 'Action for %s found after uninstallation' % ptype.getId())

    def test_skins_uninstall(self):
        self.qi.uninstallProducts([PRODUCT])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT), True,'qSEOptimizer is already installed')
        skinstool=getToolByName(self.portal, 'portal_skins') 

        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map( string.strip, string.split( path,',' ) )
            self.assert_(not PRODUCT in path, 'qSEOptimizer layer found in %s after uninstallation' %skin)

    def test_versionedskin_uninstall(self):
        self.qi.uninstallProducts([PRODUCT])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT), True,'qSEOptimizer is already installed')
        skinstool=getToolByName(self.portal, 'portal_skins')
        mtool = getToolByName(self.portal, 'portal_migration')
        plone_version = mtool.getFileSystemVersion()

        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map( string.strip, string.split( path,',' ) )
            self.assert_(not PRODUCT+'/%s' % plone_version in path, 'qSEOptimizer versioned layer found in %s after uninstallation' %skin)

    def test_configlet_uninstall(self):
        self.qi.uninstallProducts([PRODUCT])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT), True,'qSEOptimizer is already installed')

        configTool = getToolByName(self.portal, 'portal_controlpanel', None)
        self.assert_(not PRODUCT in [a.getId() for a in configTool.listActions()], 'Configlet found after uninstallation')

class TestResponse(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.qi = self.portal.portal_quickinstaller
        self.qi.installProduct(PRODUCT)
        self.portal.changeSkin('Plone Default')

        self.basic_auth = 'mgr:mgrpw'
        self.loginAsPortalOwner()

        '''Preparation for functional testing'''
        my_doc = self.portal.invokeFactory('Document', id='my_doc')
        my_doc = self.portal['my_doc']

        my_doc.qseo_properties_edit(title='hello world', description='it is description',
                                    keywords='my1|key2', html_comment='no comments',
                                    robots='ALL', distribution='Global', title_override=1,
                                    description_override=1, keywords_override=1,
                                    html_comment_override=1, robots_override=1,
                                    distribution_override=1)

        wf_tool = self.portal.portal_workflow
        wf_tool.doActionFor(my_doc, 'publish')

        abs_path = "/%s" % my_doc.absolute_url(1)
        self.html = self.publish(abs_path, self.basic_auth).getBody()

    def testTitle(self):
        m = re.match('.*<title>\\s*hello world\\s*</title>', self.html, re.S|re.M)
        self.assert_(m, 'Title not set in')

    def testDescription(self):
        m = re.match('.*<meta content="it is description" name="description" />', self.html, re.S|re.M)
        self.assert_(m, 'Description not set in')

    def testKeywords(self):
        m = re.match('.*<meta content="my1|key2" name="keywords" />', self.html, re.S|re.M)
        self.assert_(m, 'Keywords not set in')

    def testRobots(self):
        m = re.match('.*<meta content="ALL" name="robots" />', self.html, re.S|re.M)
        self.assert_(m, 'Robots not set in')

    def testDistribution(self):
        m = re.match('.*<meta content="Global" name="distribution" />', self.html, re.S|re.M)
        self.assert_(m, 'Distribution not set in')

    def testHTMLComments(self):
        m = re.match('.*<!--\\s*no comments\\s*-->', self.html, re.S|re.M)
        self.assert_(m, 'Comments not set in')
    
    def testTagsOrder(self):
        m = re.search('name="description".+name="keywords"', self.html, re.S|re.M)
        self.assert_(m, "Meta tags order not supported.")

class TestExposeDCMetaTags(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.qi = self.portal.portal_quickinstaller
        self.sp = self.portal.portal_properties.site_properties
        self.qi.installProduct(PRODUCT)
        self.portal.changeSkin('Plone Default')

        self.basic_auth = 'portal_manager:secret'
        uf = self.app.acl_users
        uf.userFolderAddUser('portal_manager', 'secret', ['Manager'], [])
        user = uf.getUserById('portal_manager')
        if not hasattr(user, 'aq_base'):
            user = user.__of__(uf)
        newSecurityManager(None, user)

        '''Preparation for functional testing'''
        self.my_doc = self.portal.invokeFactory('Document', id='my_doc')
        self.my_doc = self.portal['my_doc']

    def test_exposeDCMetaTags_in_configletOn(self):
        path = self.portal.id+'/prefs_qseo_setup?exposeDCMetaTags=on'
        self.publish(path, self.basic_auth)
        self.assert_(self.sp.exposeDCMetaTags)

    def test_exposeDCMetaTags_in_configletOff(self):
        self.publish(self.portal.id+'/prefs_qseo_setup', self.basic_auth)
        self.assert_(not self.sp.exposeDCMetaTags)

    def test_exposeDCMetaTagsPropertyOff(self):
        self.sp.manage_changeProperties(exposeDCMetaTags = False)

        self.my_doc.qseo_properties_edit()
        self.html = str(self.publish(self.portal.id+'/my_doc', self.basic_auth))

        m = re.match('.*<meta content=".*?" name="DC.format" />', self.html, re.S|re.M) or re.match('.*<meta content=".*?" name="DC.distribution" />', self.html, re.S|re.M)
        self.assert_(not m, 'DC meta tags avaliable when exposeDCMetaTags=False')

    def test_exposeDCMetaTagsPropertyOn(self):
        self.sp.manage_changeProperties(exposeDCMetaTags = True)

        self.my_doc.qseo_properties_edit()
        self.html = str(self.publish(self.portal.id+'/my_doc', self.basic_auth))

        m = re.match('.*<meta content=".*?" name="DC.format" />', self.html, re.S|re.M) and re.match('.*<meta content=".*?" name="DC.distribution" />', self.html, re.S|re.M)

        self.assert_(m, 'DC meta tags not avaliable when createManager=True')

TESTS = [TestInstallation, TestResponse, TestExposeDCMetaTags]

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    suite.addTest(makeSuite(TestResponse))
    suite.addTest(makeSuite(TestExposeDCMetaTags))
    return suite

if __name__ == '__main__':
    framework()

