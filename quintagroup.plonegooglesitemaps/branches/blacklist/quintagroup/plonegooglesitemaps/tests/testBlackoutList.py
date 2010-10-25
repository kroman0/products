#
# Tests related to general Sitemap type.
#
from base import *
from types import ListType, TupleType
from zope.component import queryUtility, queryMultiAdapter

from Products.CMFPlone.utils import _createObjectByType
from quintagroup.plonegooglesitemaps.config import BLACKOUT_PREFIX
from quintagroup.plonegooglesitemaps.interfaces import IBlackoutFilterUtility

idfname = BLACKOUT_PREFIX + "id"
pathfname = BLACKOUT_PREFIX + "path"

class TestBOFilterUtilities(TestCase):

    def testDefaultIdUtility(self):
        self.assertTrue(queryUtility(IBlackoutFilterUtility, name=idfname) is not None,
            "Not registered default '%s' IBlackoutFilterUtility" % idfname)

    def testDefaultPathUtility(self):
        self.assertTrue(queryUtility(IBlackoutFilterUtility, name=pathfname) is not None,
            "Not registered default '%s' IBlackoutFilterUtility" % pathfname)


class TestFilterMixin(TestCase):

    def afterSetUp(self):
        super(TestFilterMixin, self).afterSetUp()
        self.createTestContent()
        self.sm = _createObjectByType('Sitemap', self.portal, id='google-sitemaps')
        self.catres = self.portal.portal_catalog(portal_type=["Document",])
        self.logout()

    def createTestContent(self):
        # Add testing content to portal
        for cont in [self.portal, self.folder]:
            for i in range(1,4):
                doc = _createObjectByType('Document', cont, id='doc%i' % i)
                doc.edit(text_format='plain', text='hello world %i' % i)
                self.workflow.doActionFor(doc, 'publish')


class TestDefaultFilters(TestFilterMixin):

    def getPreparedLists(self, fname, fargs, checkindex):
        futil = queryUtility(IBlackoutFilterUtility, name=fname)
        filtered = [f.getPath() for f in futil.filterOut(self.catres, fkey=fargs)]
        catpaths = [c.getPath() for c in self.catres]
        excluded = [c.getPath() for c in self.catres if checkindex(c) == fargs]
        map(lambda l:l.sort(), [catpaths, filtered, excluded])
        return catpaths, filtered, excluded

    def testIdFilter(self):
        catpaths, filtered, excluded = self.getPreparedLists(idfname, "doc1",
            lambda b: b.id)
        self.assertTrue(type(filtered) in [ListType, TupleType],
            'Object type, returned by filteredOut method of "%s" utility '\
            'not list nor tuple' % idfname)
        self.assertTrue(set(catpaths)-set(filtered) == set(excluded),
            'Wrong filtered-out by "%s" filter:\nsrc %s\nres %s\nexcluded %s' % (
             idfname, catpaths, filtered, excluded))

    def testPathFilter(self):
        catpaths, filtered, excluded = self.getPreparedLists(pathfname,
            "/plone/doc1", lambda b: b.getPath())
        self.assertTrue(type(filtered) in [ListType, TupleType],
            'Object type, returned by filteredOut method of "%s" utility '\
            'not list nor tuple' % pathfname)
        self.assertTrue(set(catpaths)-set(filtered) == set(excluded),
            'Wrong filtered-out by "%s" filter:\nsrc %s\nres %s\nexcluded %s' % (
             pathfname, catpaths, filtered, excluded))

    def testRelativePathFilter(self):
        # 
        fpath = '/'.join(self.folder.getPhysicalPath())
        futil = queryUtility(IBlackoutFilterUtility, name=pathfname)
        sm = _createObjectByType('Sitemap', self.folder, id='google-sitemaps')
        
        fres = futil.filterOut(self.catres, fkey="./doc1", sitemap=sm)
        filtered = [f.getPath() for f in fres]
        catpaths = [c.getPath() for c in self.catres]
        excluded = [c.getPath() for c in self.catres if c.getPath()==fpath+"/doc1"]
        map(lambda l:l.sort(), [catpaths, filtered, excluded])

        self.assertTrue(type(filtered) in [ListType, TupleType],
            'Object type, returned by filteredOut method of "%s" utility '\
            'not list nor tuple' % pathfname)
        self.assertTrue(set(catpaths)-set(filtered) == set(excluded),
            'Wrong filtered-out by "%s" filter:\nsrc %s\nres %s\nexcluded %s' % (
             pathfname, catpaths, filtered, excluded))


class TestBlacklistFormProcessing(TestFilterMixin):

    def afterSetUp(self):
        super(TestBlacklistFormProcessing, self).afterSetUp()
        self.loginAsPortalOwner()
        self.smview = queryMultiAdapter((self.sm, self.app.REQUEST), name="sitemap.xml")

    def getPreparedLists(self, bl, fargs, checkindex):
        self.sm.edit(blackout_list=bl)
        filtered = [f['url'] for f in self.smview.results()]
        catpaths = [c.getURL() for c in self.catres]
        excluded = [c.getURL() for c in self.catres if checkindex(c) == fargs]
        map(lambda l:l.sort(), [catpaths, filtered, excluded])
        return catpaths, filtered, excluded

    def testGetNamedFilterUtility(self):
        catpaths, filtered, excluded = self.getPreparedLists("path:/plone/doc1",
            "/plone/doc1", lambda b: b.getPath())
        self.assertTrue(set(catpaths)-set(filtered) == set(excluded),
            'Wrong filtered-out by "%s" filter:\nsrc %s\nres %s\nexcluded %s' % (
             idfname, catpaths, filtered, excluded))

    def testDefaultFilterUtility(self):
        catpaths, filtered, excluded = self.getPreparedLists("id:doc1",
            "doc1", lambda b: b.id)
        self.assertTrue(set(catpaths)-set(filtered) == set(excluded),
            'Wrong filtered-out by "%s" filter:\nsrc %s\nres %s\nexcluded %s' % (
             idfname, catpaths, filtered, excluded))
        # Now check is output of unnamed filter same to id-named one.
        self.sm.edit(blackout_list="doc1")
        filtered_def = [f['url'] for f in self.smview.results()]
        filtered_def.sort()
        self.assertTrue(filtered == filtered_def,
            'Output of named "id" filter is not same to unnamed one:' \
            'id-named: %s\nunnamed: %s' % (filtered, filtered_def))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBOFilterUtilities))
    suite.addTest(makeSuite(TestDefaultFilters))
    suite.addTest(makeSuite(TestBlacklistFormProcessing))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
#    framework()
