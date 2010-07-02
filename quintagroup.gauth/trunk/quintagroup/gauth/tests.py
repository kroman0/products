import re
import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import quintagroup.gauth

class GauthLayer(PloneSite):
    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        ztc.installPackage(quintagroup.gauth)
        fiveconfigure.debug_mode = False

    @classmethod
    def tearDown(cls):
        pass


class TestCase(ptc.PloneTestCase):
    layer = GauthLayer


class FunctionalTestCase(ptc.FunctionalTestCase):
    layer = GauthLayer

    def _getauth(self):
        # Fix authenticator for the form
        try:
            authenticator = self.portal.restrictedTraverse("@@authenticator")
        except:
            handle  = ""
        else:
            html = authenticator.authenticator()
            handle = re.search('value="(.*)"', html).groups()[0]
        return handle


class TestInstall(TestCase):
    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct("quintagroup.gauth")
        
    def testProperties(self):
        pp = self.portal.portal_properties
        self.assert_("gauth_properties" in pp.objectIds())
        self.assert_(bool(pp.gauth_properties.hasProperty("gauth_email")))

    def testConfiglet(self):
        cp = self.portal.portal_controlpanel
        aifs = [ai['id'] for ai in cp.listActionInfos(
                check_visibility=0, check_permissions=0, check_condition=0)]
        self.assert_("quintagroup.gauth" in aifs, aifs)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstall))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
