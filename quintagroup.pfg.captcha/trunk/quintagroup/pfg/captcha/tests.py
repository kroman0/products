import re
import string
import unittest

from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase import PloneTestCase as ptc

PRODUCTS = [
    'Products.PloneFormGen',
    'quintagroup.captcha.core',
    'quintagroup.pfg.captcha',
]
PROFILES = [p+':default' for p in PRODUCTS]

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import quintagroup.pfg.captcha
    zcml.load_config('configure.zcml', quintagroup.pfg.captcha)
    fiveconfigure.debug_mode = False
    ztc.installPackage('quintagroup.pfg.captcha')
    ztc.installPackage('quintagroup.captcha.core')

setup_product()
ptc.setupPloneSite(extension_profiles=PROFILES)


class TestInstallations(ptc.PloneTestCase):

    def testInstalledProducts(self):
        qi = self.portal.portal_quickinstaller
        installed = [p['id'] for p in qi.listInstalledProducts()]
        for p in PRODUCTS:
            if p.startswith('Products'):
                p = p[9:]
            self.assertEqual(p in installed, True,
                '"%s" product not installed' % p)

    def testType(self):
        pt = self.portal.portal_types
        self.assertEqual("CaptchaField" in pt.objectIds(), True)

    def testPortalFactory(self):
        pf = self.portal.portal_factory
        self.assertEqual("CaptchaField" in pf.getFactoryTypes(), True)

    def testWorkflow(self):
        pw = self.portal.portal_workflow
        default_chain = pw.getDefaultChain()
        cf_chain = pw.getChainForPortalType('CaptchaField')
        self.assertNotEqual(cf_chain == default_chain , True)

    def testNotToList(self):
        navtree = self.portal.portal_properties.navtree_properties
        mtNotToList = navtree.getProperty("metaTypesNotToList")
        self.assertEqual('CaptchaField' in mtNotToList, True)

    def testSkins(self):
        ps = self.portal.portal_skins
        self.assertEqual("qplonecaptchafield" in ps.objectIds(), True)
        for sname, spath in ps.getSkinPaths():
            paths = filter(None, map(string.strip, spath.split(',')))
            self.assertEqual("qplonecaptchafield" in paths, True,
                '"qplonecaptchafield" layer not present in "%s" skin' % sname)

            

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestInstallations))
    return suite
