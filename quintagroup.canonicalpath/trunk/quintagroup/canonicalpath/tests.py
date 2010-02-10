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

from Products.Archetypes.tests.utils import makeContent

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
        my_doc = makeContent(self.portal, portal_type='Document', id='my_doc')
        self.logout()

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

    def testIndexer(self):
        self.loginAsPortalOwner()
        my_doc = makeContent(self.portal, portal_type='Document', id='my_doc')
        my_doc.update(title='My document')

        cpadapter = queryAdapter(my_doc, ICanonicalPath)
        cpmydoc = cpadapter.canonical_path()
        cpbrain = self.catalog(path='/'+my_doc.absolute_url(1))[0].canonical_path
        self.assertTrue(cpmydoc == cpbrain,
            "Canonical Path from adapter: '%s' not equals with brains data: '%s'" % (
             cpmydoc, cpbrain))

        self.logout()

    def testCatalogUpdateOnInstallation(self):
        self.loginAsPortalOwner()
        fp = self.portal['front-page']
        cpadapter = queryAdapter(fp, ICanonicalPath)
        cpfp = cpadapter.canonical_path()
        cpbrain = self.catalog(path='/'+fp.absolute_url(1))[0].canonical_path
        self.assertTrue(cpfp == cpbrain,
            "Catalog not updated on installation: canonical path from adapter: " \
            "'%s' not equal to brain data: '%s'" % (cpfp, cpbrain))

        self.logout()


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestAdapter),
        unittest.makeSuite(TestInstallation),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
