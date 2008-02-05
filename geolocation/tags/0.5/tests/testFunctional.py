
""" This module contains class that tests some scripts and templates in skins directory """

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestFunctional(PloneTestCase.FunctionalTestCase):
    """ Class for functional testing """

    def afterSetUp(self):
        """ AfterSetUp features """
        self.loginAsPortalOwner()
        self.membership = getToolByName(self.portal, 'portal_membership', None)
        self.membership.addMember('another_member', user_password , ['Member'], [])
        self.auth = 'portal_owner:secret'
        self.folder.invokeFactory('Document', 'test_page')
        self.page = self.folder.test_page

    def sendRequest(self, path, params={}, method="POST"):
        """ Utility function """
        return self.publish(path, self.auth, extra=params, request_method=method)

    def testSaveLocation(self):
        """ Test save_location.cpy script """
        response = self.sendRequest('%s/save_location' % self.page.absolute_url_path(),
                                    {'latitude'     : LATITUDE,
                                     'longitude'    : LONGITUDE,
                                     'maplatitude'  : MAP_CENTER[0],
                                     'maplongitude' : MAP_CENTER[1],
                                     'mapzoom'      : MAP_ZOOM,
                                     'maptype'      : MAP_TYPE}, "POST")
        self.failUnlessEqual(response.getStatus(), 200) # OK
        self.failUnlessEqual(IGEOLocated(self.page).getLatitude(), LATITUDE,
                             "save_location.cpy script work incorrectly")
        self.failUnlessEqual(IGEOMap(self.page).getMapCenter(), MAP_CENTER,
                             "save_location.cpy script work incorrectly")


    def testLocationValidatorGoodInput(self):
        """ Test validate_location.vpy script with good input """
        from Products.CMFFormController.ControllerState import ControllerState
        response = self.sendRequest('%s/validate_location' % self.portal.id,
                                    {'controller_state' : ControllerState(),
                                     'latitude'         : LATITUDE,
                                     'longitude'        : LONGITUDE}, "POST")
        self.failUnlessEqual(response.getStatus(), 200) # OK
        self.failIf(response.getBody().find('status = success') == -1,
                    "location validator didn't return success status with good input")

    def testLocationValidatorBadInput(self):
        """ Test validate_location.vpy script with bad input """
        from Products.CMFFormController.ControllerState import ControllerState
        response = self.sendRequest('%s/validate_location' % self.portal.id,
                                    {'controller_state' : ControllerState(),
                                     'latitude'         : 90.1,
                                     'longitude'        : LONGITUDE}, "POST")
        self.failUnlessEqual(response.getStatus(), 200) # OK
        self.failIf(response.getBody().find('status = failure') == -1,
                    "location validator didn't return failure status with bad input")

    def testMapValidatorGoodInput(self):
        """ Test validate_map.vpy script with good input """
        from Products.CMFFormController.ControllerState import ControllerState
        response = self.sendRequest('%s/validate_map' % self.portal.id,
                                    {'controller_state' : ControllerState(),
                                     'maplatitude'         : LATITUDE,
                                     'maplongitude'        : LONGITUDE,
                                     'mapzoom'             : MAP_ZOOM,
                                     'maptype'             : MAP_TYPE}, "POST")
        self.failUnlessEqual(response.getStatus(), 200) # OK
        self.failIf(response.getBody().find('status = success') == -1,
                    "map validator didn't return success status with good input")

    def testMapValidatorBadInput(self):
        """ Test validate_map.vpy script with bad input """
        from Products.CMFFormController.ControllerState import ControllerState
        response = self.sendRequest('%s/validate_map' % self.portal.id,
                                    {'controller_state' : ControllerState(),
                                     'maplatitude'         : LATITUDE,
                                     'maplongitude'        : -180.05,
                                     'mapzoom'             : MAP_ZOOM,
                                     'maptype'             : MAP_TYPE}, "POST")
        self.failUnlessEqual(response.getStatus(), 200) # OK
        self.failIf(response.getBody().find('status = failure') == -1,
                    "map validator didn't return failure status with bad input")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFunctional))
    return suite

if __name__ == '__main__':
    framework()
