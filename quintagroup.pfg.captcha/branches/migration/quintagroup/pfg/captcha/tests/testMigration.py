from base import *
from Products.PloneTestCase.setup import cleanupPloneSite
from Products.PloneTestCase.setup import portal_name
from Products.PloneTestCase.setup import SiteCleanup

class TestMigration(TestCaseNotInstalled):

    def installPFGCaptcha(self):
        for p in REQUIREMENTS:
            self.addProduct(p)

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def test1(self):
        qi = self.portal.portal_quickinstaller
        import pdb;pdb.set_trace()
        self.assert_(not qi.isProductInstalled("quintagroup.pfg.captcha"))
        self.installPFGCaptcha()
        self.assert_(qi.isProductInstalled("quintagroup.pfg.captcha"))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMigration))
    return suite
