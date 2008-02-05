
""" This module contains class that tests python script in portal root """

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestFunctional(PloneTestCase.FunctionalTestCase):
    """ Class for functional testing """

    def afterSetUp(self):
        """ AfterSetUp features """

        self.auth = 'admin:secret'
        self.loginAsPortalOwner()
        self.membership = self.portal.portal_membership
        self.path = '%s/%s' % (self.portal.id, EXTERNAL_METHOD)
        for m in PORTAL_MEMBERS:
            addMember(self, m['id'], m['fullname'], m['email'], m['roles'], m['last_login_time'])

    def testExternalMethod(self):
        """ Test external method script for publishing """

        if cmfmember_installed:
            getToolByName(self.portal, 'cmfmember_control').upgrade(swallow_errors=0)
        response = self.publish(self.path, self.auth, extra={'exclude_props':[], 'include_props':INCLUDE_PROPS})
        forCompare = parseCSV(self, response.getBody())
        self.failUnless(forCompare[0] == forCompare[1], '%s external method return bad CSV value' % EXTERNAL_METHOD)

    def testContentDispositionResponseHeader(self):
        """ Test response for content-disposition header """

        import re
        pattern = re.compile(r'\s*attachment\;\s*filename=\s*memberdata\-\d{4}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\.csv\s*', re.I)
        response = self.publish(self.path, self.auth, extra={'exclude_props':[], 'include_props':INCLUDE_PROPS})
        self.failUnless(pattern.search(response.getHeader('content-disposition')),
                                       'Bad response header \'Content Disposition\'')

    def testContentTypeResponseHeader(self):
        """ Test response for content-type header """

        response = self.publish(self.path, self.auth, extra={'exclude_props':[], 'include_props':INCLUDE_PROPS})
        self.failUnless(response.getHeader('content-type').find('text/csv') != -1,
                        'Bad response header \'Content Type\'')

    def testExternalMethodSecurity(self):
        """ Test external method for 'View' permission """

        response = self.publish(self.path, 'barney:secret')
        type_header = response.getHeader('bobo-exception-type')
        location_header = response.getHeader('location') or ''
        self.failUnless(type_header == 'Unauthorized' or location_header.find('login_form') != -1,
                        'Anonymous user have access to external method')

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFunctional))
    return suite

if __name__ == '__main__':
    framework()
