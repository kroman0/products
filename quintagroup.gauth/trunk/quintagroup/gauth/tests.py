import re
import sys
import unittest
import gdata.service

from zope.component import queryUtility, queryAdapter
from zope.component import getSiteManager, getGlobalSiteManager
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.PloneTestCase import portal_owner
from Products.PloneTestCase.PloneTestCase import default_password

ptc.setupPloneSite()

import quintagroup.gauth
from quintagroup.gauth.utility import SafeQuery
from quintagroup.gauth.interfaces import IGAuthUtility
from quintagroup.gauth.browser.configlet import IGAuthConfigletSchema

class GauthLayer(PloneSite):
    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        import quintagroup.gauth
        zcml.load_config('configure.zcml', quintagroup.gauth)
        fiveconfigure.debug_mode = False
        ztc.installPackage("quintagroup.gauth")

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
        gsm = getGlobalSiteManager()
        lgauth = lsm.queryUtility(IGAuthUtility)
        ggauth = gsm.queryUtility(IGAuthUtility)
        self.assertEqual(ggauth, None)
        self.assertNotEqual(lgauth, None)

    def testActionIcons(self):
        ait = self.portal.portal_actionicons
        ai = ait.getActionInfo("controlpanel", "quintagroup.gauth")
        self.assertNotEqual(ai, None)


class TestUninstall(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct("quintagroup.gauth")
        qi = self.portal.portal_quickinstaller
        # qi.installProducts(products=["quintagroup.gauth",])
        qi.uninstallProducts(products=["quintagroup.gauth",])

    def testProperties(self):
        pp = self.portal.portal_properties
        self.assert_(not "gauth_properties" in pp.objectIds())

    def testConfiglet(self):
        cp = self.portal.portal_controlpanel
        aifs = [ai['id'] for ai in cp.listActionInfos(
                check_visibility=0, check_permissions=0, check_condition=0)]
        self.assert_(not "quintagroup.gauth" in aifs)

    def testUtility(self):
        lsm = getSiteManager(self.portal)
        gsm = getGlobalSiteManager()
        lgauth = lsm.queryUtility(IGAuthUtility)
        ggauth = gsm.queryUtility(IGAuthUtility)
        self.assertEqual(ggauth, None)
        self.assertEqual(lgauth, None)

    def testActionIcons(self):
        ait = self.portal.portal_actionicons
        ai = ait.queryActionInfo("controlpanel", "quintagroup.gauth", default=None)
        self.assert_(ai == None)


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


class TestUtility(FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct("quintagroup.gauth")
        sm = getSiteManager(self.portal)
        self.gauthutil = sm.queryUtility(IGAuthUtility)
        self.gauthconfiglet = queryAdapter(self.portal, IGAuthConfigletSchema)

    def testEmail(self):
        self.assertEqual(bool(self.gauthutil.email), False)
        self.gauthconfiglet.gauth_email = "tester@test.com"
        self.assertEqual(self.gauthutil.email, "tester@test.com")

    def testPassword(self):
        self.assertEqual(bool(self.gauthutil.password), False)
        self.gauthconfiglet.gauth_pass = u"secret"
        self.assertEqual(self.gauthutil.password, "secret")


out = ""
class DummyService(object):
    doraise = False

    def ProgrammaticLogin(self):
        global out
        out += "\nCall ProgrammaticLogin"
        self.doraise = False

    def Action(self, *args, **kwargs):
        global out
        out += "\nCall Action with: args='%s', kwargs='%s'" % (str(args), str(kwargs))
        if self.doraise:
            raise gdata.service.RequestError("Token is expired")

class TestSafeQuery(unittest.TestCase):

    def setUp(self):
        global out
        self.serv = DummyService()
        self.args = "test_arg",
        self.kwargs = {"kw1_key": "kw1_val"}
        self.sq = SafeQuery()
        out = ""

    def testMethodCall(self):
        self.sq.safeQuery(self.serv, self.serv.Action, *self.args, **self.kwargs)
        res = filter(None, out.split("\n"))
        self.assertEqual(res[0],
            "Call Action with: args='%s', kwargs='%s'" % (str(self.args), str(self.kwargs)))

    def testProgrammaticLogin(self):
        self.serv.doraise = True
        self.sq.safeQuery(self.serv, self.serv.Action, *self.args, **self.kwargs)
        res = filter(None, out.split("\n"))
        self.assertEqual(res[0], "Call Action with: args='%s', kwargs='%s'" % (
            str(self.args), str(self.kwargs)))
        self.assertEqual(res[1], "Call ProgrammaticLogin")
        self.assertEqual(res[2], "Call Action with: args='%s', kwargs='%s'" % (
            str(self.args), str(self.kwargs)))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstall))
    suite.addTest(makeSuite(TestUninstall))
    suite.addTest(makeSuite(TestConfiglet))
    suite.addTest(makeSuite(TestUtility))
    suite.addTest(makeSuite(TestSafeQuery))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
