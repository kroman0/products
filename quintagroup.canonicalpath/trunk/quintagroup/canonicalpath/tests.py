import unittest

from zope.testing import doctestunit
from zope.component import testing
from zope.component import queryAdapter, queryMultiAdapter
from zope.schema.interfaces import InvalidValue
from plone.indexer.interfaces import IIndexableObject
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

from Products.Archetypes.tests.utils import makeContent

from quintagroup.canonicalpath.interfaces import ICanonicalPath
from quintagroup.canonicalpath.interfaces import ICanonicalLink
from quintagroup.canonicalpath.adapters import PROPERTY_PATH
from quintagroup.canonicalpath.adapters import PROPERTY_LINK

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            import quintagroup.canonicalpath
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', quintagroup.canonicalpath)
            fiveconfigure.debug_mode = False

ptc.setupPloneSite()

class TestIndexerRegistration(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.my_doc = makeContent(self.portal, portal_type='Document', id='my_doc')
        self.logout()

    def testForPortal(self):
        wrapper = queryMultiAdapter((self.portal, self.catalog), IIndexableObject)
        self.assertFalse(wrapper is None, "No indexer registered for portal object")

    def testForAT(self):
        wrapper = queryMultiAdapter((self.my_doc, self.catalog), IIndexableObject)
        self.assertFalse(wrapper is None, "No indexer registered for document object")

    def testCanonicalPathForPortal(self):
        wrapper = queryMultiAdapter((self.portal, self.catalog), IIndexableObject)
        self.assertTrue(hasattr(wrapper, 'canonical_path'),
            "'canonical_path' attribute not accessible with indexer wrapper for portal object")

    def testCanonicalPathForAT(self):
        wrapper = queryMultiAdapter((self.my_doc, self.catalog), IIndexableObject)
        self.assertTrue(hasattr(wrapper, 'canonical_path'),
            "'canonical_path' attribute not accessible with indexer wrapper for Document object")

    def testCanonicalLinkForPortal(self):
        wrapper = queryMultiAdapter((self.portal, self.catalog), IIndexableObject)
        self.assertTrue(hasattr(wrapper, 'canonical_link'),
            "'canonical_link' attribute not accessible with indexer wrapper for portal object")

    def testCanonicalLinkForAT(self):
        wrapper = queryMultiAdapter((self.my_doc, self.catalog), IIndexableObject)
        self.assertTrue(hasattr(wrapper, 'canonical_link'),
            "'canonical_link' attribute not accessible with indexer wrapper for Document object")


        
class TestDefaultCanonicalPathAdapter(TestCase):


    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.purl = getToolByName(self.portal, 'portal_url')
        self.my_doc = makeContent(self.portal, portal_type='Document', id='my_doc')
        self.logout()

        self.mydoc_cp = '/'+'/'.join(self.purl.getRelativeContentPath(self.my_doc))
        self.portal_cp = '/'+'/'.join(self.purl.getRelativeContentPath(self.portal))

    def testRegistration4Portal(self):
        cpadapter = queryAdapter(self.portal, ICanonicalPath)
        self.assertFalse(cpadapter is None,
            "Can't get canonical path adapter for the plone site object")

    def testRegistration4AT(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        self.assertFalse(cpadapter is None,
            "Can't get canonical path adapter for the Document object")
        

    def testGetDefault4Portal(self):
        cpadapter = queryAdapter(self.portal, ICanonicalPath)
        self.assertTrue(cpadapter.canonical_path == self.portal_cp,
            "Canonical path adapter return '%s' for portal, must be: '%s'" % (
            cpadapter.canonical_path, self.portal_cp) )


    def testGetDefault4AT(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        self.assertTrue(cpadapter.canonical_path == self.mydoc_cp,
            "Canonical path adapter return '%s' for document, must be: '%s'" % (
            cpadapter.canonical_path, self.mydoc_cp) )


    def testSet4Portal(self):
        cpadapter = queryAdapter(self.portal, ICanonicalPath)
        newcp = self.portal_cp + '/new_portal_canonical'

        cpadapter.canonical_path = newcp
        prop = self.portal.getProperty(PROPERTY_PATH, None)
        self.assertTrue(prop == newcp,
            "Canonical path adapter setter NOT SET new '%s' value to '%s' " \
            "propery for the portal" % (newcp, PROPERTY_PATH) )

        self.assertTrue(cpadapter.canonical_path == newcp,
            "Canonical path adapter GET '%s' canonical_path, for portal, " \
            "must be: '%s'" % (cpadapter.canonical_path, newcp) )


    def testSet4AT(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        newcp = self.mydoc_cp + '/new_mydoc_canonical'

        cpadapter.canonical_path = newcp
        prop = self.my_doc.getProperty(PROPERTY_PATH, None)
        self.assertTrue(prop == newcp,
            "Canonical path adapter setter NOT SET new '%s' value to '%s' " \
            "propery for the Document" % (newcp, PROPERTY_PATH) )

        self.assertTrue(cpadapter.canonical_path == newcp,
            "Canonical path adapter GET '%s' canonical_path, for Document, " \
            "must be: '%s'" % (cpadapter.canonical_path, newcp) )


    def testValidationWrong(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        for wrong in ['new\nline','s p a c e','with\ttabs']:
            try:
                cpadapter.canonical_path = wrong
            except InvalidValue:
                continue
            else:
                raise self.failureException, "InvalidValue not raised when '%s' wrong value try to set" % wrong
        
    def testValidationGood(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        for good in ['./good','../good','/good', 'good']:
            cpadapter.canonical_path = good


class TestDefaultCanonicalLinkAdapter(TestCase):


    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.purl = getToolByName(self.portal, 'portal_url')
        self.my_doc = makeContent(self.portal, portal_type='Document', id='my_doc')
        self.logout()

        self.mydoc_cl = self.my_doc.absolute_url()

    def testRegistration4Portal(self):
        cladapter = queryAdapter(self.portal, ICanonicalLink)
        self.assertFalse(cladapter is None,
            "Can't get canonical link adapter for the plone site object")

    def testRegistration4AT(self):
        cladapter = queryAdapter(self.my_doc, ICanonicalLink)
        self.assertFalse(cladapter is None,
            "Can't get canonical link adapter for the Document object")
        

    def testGetDefault4Portal(self):
        cladapter = queryAdapter(self.portal, ICanonicalLink)
        self.assertTrue(cladapter.canonical_link == self.purl(),
            "Canonical link adapter return '%s' for portal, must be: '%s'" % (
            cladapter.canonical_link, self.purl()) )


    def testGetDefault4AT(self):
        cladapter = queryAdapter(self.my_doc, ICanonicalLink)
        self.assertTrue(cladapter.canonical_link == self.mydoc_cl,
            "Canonical link adapter return '%s' for document, must be: '%s'" % (
            cladapter.canonical_link, self.mydoc_cl) )


    def testSet4Portal(self):
        cladapter = queryAdapter(self.portal, ICanonicalLink)
        newcl = self.purl() + '/new_portal_canonical'

        cladapter.canonical_link = newcl
        prop = self.portal.getProperty(PROPERTY_LINK, None)
        self.assertTrue(prop == newcl,
            "Canonical link adapter setter NOT SET new '%s' value to '%s' " \
            "propery for the portal" % (newcl, PROPERTY_LINK) )

        self.assertTrue(cladapter.canonical_link == newcl,
            "Canonical link adapter GET '%s' canonical_link, for portal, " \
            "must be: '%s'" % (cladapter.canonical_link, newcl) )


    def testSet4AT(self):
        cladapter = queryAdapter(self.my_doc, ICanonicalLink)
        newcl = self.mydoc_cl + '/new_mydoc_canonical'

        cladapter.canonical_link = newcl
        prop = self.my_doc.getProperty(PROPERTY_LINK, None)
        self.assertTrue(prop == newcl,
            "Canonical link adapter setter NOT SET new '%s' value to '%s' " \
            "propery for the Document" % (newcl, PROPERTY_LINK) )

        self.assertTrue(cladapter.canonical_link == newcl,
            "Canonical link adapter GET '%s' canonical_link, for Document, " \
            "must be: '%s'" % (cladapter.canonical_link, newcl) )

    def testValidationWrong(self):
        cladapter = queryAdapter(self.my_doc, ICanonicalLink)
        for wrong in ['http://new\nline','s p a c e','with\ttabs']:
            try:
                cladapter.canonical_link = wrong
            except InvalidValue:
                continue
            else:
                raise self.failureException, "InvalidValue not raised when " \
                    "'%s' wrong value try to set" % wrong
        
    def testValidationGood(self):
        cladapter = queryAdapter(self.my_doc, ICanonicalLink)
        for good in ['http://', './good','../good','/good', 'good']:
            cladapter.canonical_link = good


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestIndexerRegistration),
        unittest.makeSuite(TestDefaultCanonicalPathAdapter),
        unittest.makeSuite(TestDefaultCanonicalLinkAdapter),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
