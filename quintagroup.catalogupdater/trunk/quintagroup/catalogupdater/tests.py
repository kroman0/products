import unittest

from zope.interface import Interface
from zope.component import queryUtility
from zope.component import provideAdapter

from plone.indexer.decorator import indexer
from plone.indexer.interfaces import IIndexableObject
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.Archetypes.tests.utils import makeContent

from quintagroup.catalogupdater.utility import ICatalogUpdater

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            import quintagroup.catalogupdater
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', quintagroup.catalogupdater)
            fiveconfigure.debug_mode = False

ptc.setupPloneSite()


class TestUtility(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.my_doc = makeContent(self.portal, portal_type='Document', id='my_doc')
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.logout()
        self.addIndexer()

    def addIndexer(self):
        @indexer(Interface)
        def test_column(obj):
            return obj.id

        provideAdapter(test_column, name='test_column')
        self.catalog.addColumn('test_column')

    def testMetadataUpdate(self):
        """ Test is metadata column updated with utility
        """
        docs = self.catalog.unrestrictedSearchResults(portal_type='Document')
        self.assertTrue([1 for b in docs if b.test_column == b.id] == [],
            "Some document has updated 'test_column' metadata in catalog: '%s'" % docs)

        cu = queryUtility(ICatalogUpdater, name="catalog_updater")
        cu.updateMetadata4All(self.catalog, 'test_column')

        docs = self.catalog.unrestrictedSearchResults(portal_type='Document')
        self.assertTrue([1 for b in docs if b.test_column != b.id] == [],
            "Some document has wrong 'test_column' metadata in catalog: '%s'" % docs)

    def testOnlyOneColumnUpdate(self):
        """ Update a title property for the my_doc object (without reindexing)
            then, after utility usage - check is that metadata is leave unchanged.
        """
        self.loginAsPortalOwner()
        self.my_doc.update(title="My document")
        self.logout()

        mydoc = self.catalog.unrestrictedSearchResults(id='my_doc')[0]
        self.assertTrue(mydoc.Title == "My document", mydoc.Title)

        self.my_doc.setTitle('New my document') # catalog not updated
        cu = queryUtility(ICatalogUpdater, name="catalog_updater")
        cu.updateMetadata4All(self.catalog, 'test_column')

        mydoc = self.catalog.unrestrictedSearchResults(id='my_doc')[0]
        self.assertTrue(mydoc.Title == 'My document',
            "Other metadata updated: Title='%s'" % mydoc.Title)

        self.assertTrue(mydoc.test_column == 'my_doc',
            "Wrong data in updated metadata: test_column='%s', " \
            "must be 'my_doc'" % mydoc.test_column)


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestUtility),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
