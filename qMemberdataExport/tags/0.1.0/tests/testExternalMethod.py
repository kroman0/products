
""" This module contains class that tests script for external method """


import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestExternalMethod(PloneTestCase.PloneTestCase):
    """ Class for testing script for external method """

    def afterSetUp(self):
        """ AfterSetUp features """

        self.loginAsPortalOwner()
        self.method = getattr(self.portal, EXTERNAL_METHOD)
        self.membership = self.portal.portal_membership
        for m in PORTAL_MEMBERS:
            addMember(self, m['id'], m['fullname'], m['email'], m['roles'], m['last_login_time'])

    def testMemberData(self):
        """ Test external script for good csv output stream """

        if cmfmember_installed:
            getToolByName(self.portal, 'cmfmember_control').upgrade(swallow_errors=0)
        forCompare = parseCSV(self, self.method(self.portal, exclude_props=EXCLUDE_PROPS, include_props=INCLUDE_PROPS))
        self.failUnless(forCompare[0] == forCompare[1], 'Bad output from external method script')

    def testExternalMethodPermissions(self):
        """ Test external method 'View' permission """

        selected = [r['name'] for r in self.method.rolesOfPermission('View') if r['selected']]
        self.failUnless(len(selected) ==1 and 'Manager' in selected,
                        'External method have bad roles for \'View\' permission')

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestExternalMethod))
    return suite

if __name__ == '__main__':
    framework()
