#
# testSetup
#

from base import *
from config import skins_content, istalled_types, types_actions

class TestSetup(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.qi = getattr(self.portal.aq_explicit, 'portal_quickinstaller')
        self.ttool = getattr(self.portal.aq_explicit, 'portal_types')
        self.ptool =  getattr(self.portal.aq_explicit, 'portal_properties')

    def test_installed_products(self):
        qi = self.qi
        installed = [ prod['id'] for prod in qi.listInstalledProducts() ]
        self.failUnless('qPingTool' in installed, installed)
        self.failUnless('Quills' in installed, installed)

    def test_tool_installed(self):
        t = getToolByName(self.portal, 'portal_pingtool', None)
        self.failUnless(t, t)
        self.failUnless(isinstance(t, PingTool.PingTool), t.__class__)
        self.failUnlessEqual(t.meta_type, 'PingTool')
        self.failUnlessEqual(t.getId(), 'portal_pingtool')

    def test_skin_installed(self):
        stool = getattr(self.portal.aq_explicit, 'portal_skins')
        ids = stool.objectIds()
        self.failUnless('qpingtool' in ids, ids)
        content = [i.id for i in self.portal.portal_skins.qpingtool.objectValues()]
        content.sort()
        skins_content.sort()
        self.failUnless(content==skins_content)

    def test_installedAllTypes(self):
        # test that all types are installed well
        ttool = self.ttool
        tids = ttool.objectIds()
        for id in istalled_types:
            self.failUnless(id in tids, (id, tids))
            tinfo = ttool[id]
            self.failUnless(tinfo.product == 'qPingTool', tinfo.product)

    def test_added_action(self):
        t = getToolByName(self.portal, 'portal_pingtool', None)
        ttool = self.ttool
        for type_actions in types_actions:
            pttool = ttool[type_actions['type']]
            for id, name, action, permission, category, visible in type_actions['actions']:
                pt_actions_ids = [a.getId() for a in pttool.listActions()]
                pt_action = [a for a in pttool.listActions() if a.id == id][0]
                self.failUnless(id in pt_actions_ids, pt_actions_ids)
                self.failUnless(name == pt_action.Title(), pt_action)
                self.failUnless(action == pt_action.getActionExpression(), pt_action)
                self.failUnless(permission == pt_action.getPermissions(), pt_action)
                self.failUnless(category == pt_action.getCategory(), pt_action)
                self.failUnless(visible == pt_action.getVisibility(), pt_action)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite
