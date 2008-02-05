
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
        #maps_login(self, user_name)
        #self.auth = user_name + ':' + user_password
        self.auth = 'portal_owner:secret'
        self.map_properties = getToolByName(self.portal, 'portal_properties').maps_properties

    def sendRequest(self, path, params={}, method="POST"):
        """ Utility function """
        return self.publish(path, self.auth, extra=params, request_method=method)

    def testPrefsMapsKeySet(self):
        """ Test prefs_maps_key_set.py script """
        response = self.sendRequest('%s/prefs_mapkeys_set' % self.portal.id, {'map_api_keys':[NEW_MAP_KEY,]}, "POST")
        self.failUnlessEqual(response.getStatus(), 302) # OK
        self.failUnlessEqual((NEW_MAP_KEY,), self.map_properties.map_api_keys,
                             "prefs_maps_key_set.py script work incorrect")

    def testGetMapKey(self):
        """ Test getMapKey.py script """
        response = self.sendRequest('%s/prefs_mapkeys_set' % self.portal.id, {'map_api_keys':[NEW_MAP_KEY,]}, "POST")
        self.failUnlessEqual(response.getStatus(), 302) # OK
        response = self.sendRequest('%s/getMapKey' % self.portal.id)
        self.failUnlessEqual(response.getStatus(), 200) # OK
        self.failUnlessEqual(response.getBody(), NEW_MAP_KEY[NEW_MAP_KEY.find('|')+1:])

    def testValidatorGoodInput(self):
        """ Test validate_mapkeys.vpy script with good input """
        from Products.CMFFormController.ControllerState import ControllerState
        response = self.sendRequest('%s/validate_mapkeys' % self.portal.id,
                                    {'controller_state':ControllerState(), 'map_api_keys':[NEW_MAP_KEY,]},
                                    "POST")
        self.failUnlessEqual(response.getStatus(), 200) # OK
        self.failIf(response.getBody().find('status = success') == -1,
                    "validator didn't return success status with good input")

    def testValidatorBadInput(self):
        """ Test validate_mapkeys.vpy script with bad input """
        from Products.CMFFormController.ControllerState import ControllerState
        response = self.sendRequest('%s/validate_mapkeys' % self.portal.id,
                                    {'controller_state':ControllerState(), 'map_api_keys':['badinput|',]},
                                    "POST")
        self.failUnlessEqual(response.getStatus(), 200) # OK
        self.failIf(response.getBody().find('status = failure') == -1,
                    "validator didn't return success status with bad input")

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFunctional))
    return suite

if __name__ == '__main__':
    framework()
