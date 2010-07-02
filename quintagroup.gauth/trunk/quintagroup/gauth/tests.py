import re
import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from zope.component import queryUtility
from zope.component import getSiteManager
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.PloneTestCase import portal_owner
from Products.PloneTestCase.PloneTestCase import default_password

ptc.setupPloneSite()

import quintagroup.gauth
from quintagroup.gauth.interfaces import IGAuthUtility

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

    def testUtility(self):
        lsm = getSiteManager(self.portal)
        gauth = lsm.queryUtility(IGAuthUtility)
        self.assert_(gauth is not None)
        self.assert_(gauth.gconf is not None)

class TestConfiglet(FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct("quintagroup.gauth")
        self.basic_auth = portal_owner + ":" + default_password
        self.get_url = self.portal.id+'/@@gauth-controlpanel'
        self.save_url = self.portal.id+'/@@gauth-controlpanel?form.actions.save=1' \
            '&_authenticator=%s' % self._getauth()

    def test_presentEmail(self):
        res = self.publish(self.get_url, self.basic_auth).getBody()
        self.assert_(re.match(".*<input\s[^>]*name=\"form.gauth_email\"[^>]*>", res, re.I|re.S))

    def test_presentPassword(self):
        res = self.publish(self.get_url, self.basic_auth).getBody()
        self.assert_(re.match(".*<input\s[^>]*name=\"form.gauth_pass\"[^>]*>", res, re.I|re.S))

    def test_update(self):
        temail, tpass = "tester@test.com", "secret"
        gauth_util = queryUtility(IGAuthUtility)
        url = self.save_url + '&form.gauth_email='+temail + '&form.gauth_pass='+tpass
        self.publish(url, self.basic_auth)
        self.assert_(gauth_util.email == temail)
        self.assert_(gauth_util.password == tpass)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstall))
    suite.addTest(makeSuite(TestConfiglet))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
