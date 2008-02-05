
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
        self.qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.qi.installProduct(PRODUCT)
        self.membership = self.portal.portal_membership
        for m in PORTAL_MEMBERS:
            addMember(self, m['id'], m['fullname'], m['email'], m['roles'], m['last_login_time'])
        self.response = self.sendRequest('%s/%s' % (self.portal.id, PYTHON_SCRIPT), {}, "GET")

    def sendRequest(self, path, params={}, method="POST"):
        """ Utility function """

        return self.publish(path, self.auth, extra=params, request_method=method)


    def testExportMemberdataScript(self):
        """ Test exportMemberData python script """

        forCompare = parseCSV(self, self.response.getBody())
        self.failUnless(forCompare[0] == forCompare[1], '%s script return bad CSV value' % PYTHON_SCRIPT)

    def testContentDispositionResponseHeader(self):
        """ Test response for content-disposition header """

        import re
        pattern = re.compile(r'\s*attachment\;\s*filename=\s*memberdata\-\d{4}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\.csv\s*', re.I)
        self.failUnless(pattern.search(self.response.getHeader('content-disposition')),
                                       'Bad response header \'Content Disposition\'')

    def testContentTypeResponseHeader(self):
        """ Test response for content-type header """

        self.failUnless(self.response.getHeader('content-type').find('text/csv') != -1,
                        'Bad response header \'Content Type\'')

    def testScriptSecurity(self):
        """ Test external script 'View' permission via python script """

        maps_login(self, 'anonym')
        response = self.publish('%s/%s' % (self.portal.id, PYTHON_SCRIPT))

        self.failUnless(response.getHeader('bobo-exception-type') == 'Unauthorized',
                        'Anonymous user have access to external method via python script')

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFunctional))
    return suite

if __name__ == '__main__':
    framework()
