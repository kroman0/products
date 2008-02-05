
""" This module contains class that tests product's installation  procedure """

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestInstallation(PloneTestCase.PloneTestCase):
    """ Class for testing installation procedure """

    def afterSetUp(self):
        """ AfterSetUp features """
        self.qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.qi.installProduct(PRODUCT)

    def testAddingExternalMethod(self):
        """ Test adding external method to portal """
        self.failUnless(EXTERNAL_METHOD in self.portal.objectIds(),
                        '%s external method does not exist in portal' % EXTERNAL_METHOD)

    def testMemberdataHandlersRegistry(self):
        """ Test registration of memberdata handlers """
        from Products.qMemberdataExport import getRegisteredMemberdataHandlers as registry
        self.failUnless(len(registry()) == 2, 'Bad registry data')

#tests.append(TestInstallation)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    return suite

if __name__ == '__main__':
    framework()
