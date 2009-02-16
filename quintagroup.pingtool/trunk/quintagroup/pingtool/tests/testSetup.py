#
# testSetup
#

from quintagroup.pingtool.config import PROJECTNAME
from base import *
from config import istalled_types

class TestSetup(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.qi = getattr(self.portal.aq_explicit, 'portal_quickinstaller')
        self.ttool = getattr(self.portal.aq_explicit, 'portal_types')
        self.ptool =  getattr(self.portal.aq_explicit, 'portal_properties')

    def test_installed_uninstalled_products(self):
        # test that package are installed/uninstalled well
        self.assertNotEqual(self.qi.isProductInstalled(PROJECTNAME), False, '%s is already installed' % PROJECTNAME)
        
        self.qi.uninstallProducts([PROJECTNAME])
        self.assertNotEqual(self.qi.isProductInstalled(PROJECTNAME), True, '%s is already installed' % PROJECTNAME)

    def test_tool_install_uninstall(self):
        # test that tool are installed/uninstalled well
        tname = 'portal_pingtool'
        t = getToolByName(self.portal, tname, None)
        self.assertNotEqual(t, False, 'Tool %s not found after installation' % tname)
        self.failUnless(t, t)
        self.failUnless(isinstance(t, PingTool.PingTool), t.__class__)
        self.failUnlessEqual(t.meta_type, 'PingTool')
        self.failUnlessEqual(t.getId(), tname)

        self.qi.uninstallProducts([PROJECTNAME])
        self.assertNotEqual(self.qi.isProductInstalled(PROJECTNAME), True, '%s is already installed' % PROJECTNAME)

        t = getToolByName(self.portal, tname, None)
	self.assertNotEqual(t, True, 'Tool %s found after uninstallation' % tname)

    def test_install_uninstall_types(self):
        # test that types are installed/uninstalled well
        ttool = self.ttool
        tids = ttool.objectIds()
        for id in istalled_types:
            self.assertNotEqual(id in tids, False, 'Type %s not found after installation' % id)
            tinfo = ttool[id]
            self.failUnless(tinfo.product == PROJECTNAME, tinfo.product)

        self.qi.uninstallProducts([PROJECTNAME])
        self.assertNotEqual(self.qi.isProductInstalled(PROJECTNAME), True, '%s is already installed' % PROJECTNAME)
        
	tids = ttool.objectIds()
        for id in istalled_types:
            self.assertNotEqual(id in tids, True, 'Type %s found after uninstallation' % id)

    def test_actions_install_uninstall(self):
        # test that actions are installed/uninstalled well
	action = 'ping'
        ttool = self.ttool
        portal_action = getToolByName(self.portal, 'portal_actions')
        object_buttons = portal_action.object_buttons
        pt_actions_ids = [a.id for a in object_buttons.listActions()]
        self.assertNotEqual(action in pt_actions_ids, False, 'Action for %s not found after installation' % action)
        
        self.qi.uninstallProducts([PROJECTNAME])
        self.assertNotEqual(self.qi.isProductInstalled(PROJECTNAME), True, '%s is already installed' % PROJECTNAME)
	
        pt_actions_ids = [a.id for a in object_buttons.listActions()]
        self.assertNotEqual(action in pt_actions_ids, True, 'Action for %s found after uninstallation' % action)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite
