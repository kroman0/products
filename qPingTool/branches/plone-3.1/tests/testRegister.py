#
# Register skins
#

from base import *

class TestSetup(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def testRegisterSkins(self):
        test_content = ['tool.gif']
        self.failUnless(not getattr(self.portal.portal_skins, 'qpingtool', None)==None)
        content = [i.id for i in self.portal.portal_skins.qpingtool.objectValues()]
        content.sort()
        test_content.sort()
        self.failUnless(content==test_content)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite
