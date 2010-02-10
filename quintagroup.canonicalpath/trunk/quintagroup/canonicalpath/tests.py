import unittest

from zope.testing import doctestunit
from zope.component import testing
from zope.component import queryAdapter
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

from quintagroup.canonicalpath.interfaces import ICanonicalPath

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            import quintagroup.canonicalpath
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', quintagroup.canonicalpath)
            fiveconfigure.debug_mode = False

ptc.setupPloneSite()

class TestAdapter(TestCase):

    def afterSetUp(self):
        self.purl = getToolByName(self.portal, 'portal_url')

    def testAdapter4Portal(self):
        cpadapter = queryAdapter(self.portal, ICanonicalPath)
        self.assertFalse(cpadapter is None,
            "Can't get canonical path adapter for the plone site object")


        portal_cp = '/'+'/'.join(self.purl.getRelativeContentPath(self.portal))
        adcp = cpadapter.canonical_path()
        self.assertTrue(adcp == portal_cp, "Canonical path adapter return '%s' "\
            "for portal, must be: '%s'" % (adcp, portal_cp) )


    def testAdapter4AT(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory('Document', id='my_doc')
        self.logout()
        my_doc = self.portal['my_doc']

        cpadapter = queryAdapter(my_doc, ICanonicalPath)
        self.assertFalse(cpadapter is None,
            "Can't get canonical path adapter for the Document object")

        mydoc_cp = '/'+'/'.join(self.purl.getRelativeContentPath(my_doc))
        adcp = cpadapter.canonical_path()
        self.assertTrue(adcp == mydoc_cp, "Canonical path adapter return '%s' "\
            "for document, must be: '%s'" % (adcp, mydoc_cp) )

class TestInstallation(TestCase):

    def afterSetUp(self):
        self.qi = self.portal.portal_quickinstaller
        self.qi.installProduct("quintagroup.canonicalpath")

        self.purl = getToolByName(self.portal, 'portal_url')
        self.catalog = getToolByName(self.portal, 'portal_catalog')

    def testCatalogMetadata(self):
        self.assertTrue('canonical_path' in self.catalog._catalog.names,
            "'canonical_path' metadata not added to catalog.")



def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestAdapter),
        unittest.makeSuite(TestInstallation),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
