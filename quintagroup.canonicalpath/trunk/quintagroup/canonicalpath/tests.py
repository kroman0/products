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
from quintagroup.canonicalpath.adapters import PROPERTY

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
        
        
class TestDefaultAdapter(TestCase):


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
        prop = self.portal.getProperty(PROPERTY, None)
        self.assertTrue(prop == newcp,
            "Canonical path adapter setter NOT SET new '%s' value to '%s' " \
            "propery for the portal" % (newcp, PROPERTY) )

        self.assertTrue(cpadapter.canonical_path == newcp,
            "Canonical path adapter GET '%s' canonical_path, for portal, " \
            "must be: '%s'" % (cpadapter.canonical_path, newcp) )


    def testSet4AT(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        newcp = self.mydoc_cp + '/new_mydoc_canonical'

        cpadapter.canonical_path = newcp
        prop = self.my_doc.getProperty(PROPERTY, None)
        self.assertTrue(prop == newcp,
            "Canonical path adapter setter NOT SET new '%s' value to '%s' " \
            "propery for the Document" % (newcp, PROPERTY) )

        self.assertTrue(cpadapter.canonical_path == newcp,
            "Canonical path adapter GET '%s' canonical_path, for Document, " \
            "must be: '%s'" % (cpadapter.canonical_path, newcp) )


    def testValidation(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        for wrong in ['new\nline','s p a c e','with\ttabs']:
            try:
                cpadapter.canonical_path = wrong
            except InvalidValue:
                continue
            else:
                raise self.failureException, "InvalidValue not raised when " \
                      "wrong value set"


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestIndexerRegistration),
        unittest.makeSuite(TestDefaultAdapter),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
