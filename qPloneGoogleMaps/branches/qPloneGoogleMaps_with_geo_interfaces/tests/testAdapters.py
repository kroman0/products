
""" This module contains class that tests MarkersListing adapter """

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestForInterfaces(PloneTestCase.PloneTestCase):
    """ Class for testing adapters' and browsers' for interfaces """

    def testAdapterInterface(self):
        """ Test adapters' for intefaces """
        verifyClass(IMarkersListing, MarkersListing)

    def testBrowserInterface(self):
        """ Test browsers' for intefaces """
        verifyClass(IMarkersView, MarkersView)

class TestMarkersListing(PloneTestCase.PloneTestCase):
    """ Class for testing MarkersListing adapter """

    def afterSetUp(self):
        """ AfterSetUp features """
        pass

    def testImplementation(self):
        """ Test adapters implementation """
        IMarkersListing.implementedBy(MarkersListing)

    def testListMarkersAdapterMethod(self):
        """ Test listMarkers adapters' method """
        maps_login(self, 'member')
        self.folder.invokeFactory('Folder', 'source_folder')
        self.folder.source_folder.invokeFactory('Document', 'test_page')
        folder_adapter = IMarkersListing(self.folder.source_folder)
        IPoint(self.folder.source_folder.test_page).coordinates = (FIELD_VALUE[0], FIELD_VALUE[1], 0)
        self.folder.source_folder.test_page.reindexObject()
        self.failUnless(folder_adapter.listMarkers()[0].getId == 'test_page',
                        "listMarkers adapters' method return incorrect value")

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestForInterfaces))
    suite.addTest(makeSuite(TestMarkersListing))
    return suite

if __name__ == '__main__':
    framework()
