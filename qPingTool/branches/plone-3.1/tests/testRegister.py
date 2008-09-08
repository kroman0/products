#
# Register skins
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from base import *

class TestSetup(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def testRegisterSkins(self):
        test_content = ['ping_setup', 'ping_now', 'save_ping_setup', 'tool.gif']
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

if __name__ == '__main__':
    framework()
