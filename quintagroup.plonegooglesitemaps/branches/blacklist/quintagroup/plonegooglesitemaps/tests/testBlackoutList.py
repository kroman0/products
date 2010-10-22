#
# Tests related to general Sitemap type.
#
from base import *
from types import ListType, TupleType
from zope.component import queryUtility

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


class TestDefaultFilters(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        # Add testing content to portal
        for cont in [self.portal, self.folder]:
            for i in range(1,4):
                doc = _createObjectByType('Document', cont, id='my_doc%i' % i)
                doc.edit(text_format='plain', text='hello world %i' % i)
        self.catres = self.portal.portal_catalog(portal_type=["Document",])
        self.logout()

    def testIdFilter(self):
        idfilter = queryUtility(IBlackoutFilterUtility, name=idfname)
        catpaths = [c.getPath() for c in self.catres]
        filtered = [f.getPath() for f in idfilter.filterOut(self.catres, fkey="my_doc1")]
        excluded = [c.getPath() for c in self.catres if c.id == "my_doc1"]
        map(lambda l:l.sort(), [catpaths, filtered, excluded])
        self.assertTrue(type(filtered) in [ListType, TupleType],
            'Object type, returned by filteredOut method of "%s" utility '\
            'not list nor tuple' % idfname)
        self.assertTrue(set(catpaths)-set(filtered) == set(excluded),
            'Wrong filtered-out by "%s" filter:\nsrc %s\nres %s\nexcluded %s' % (
             idfname, catpaths, filtered, excluded))

    def testPathFilter(self):
        pathfilter = queryUtility(IBlackoutFilterUtility, name=pathfname)
        catpaths = [c.getPath() for c in self.catres]
        filtered = [f.getPath() for f in pathfilter.filterOut(self.catres, fkey="/plone/my_doc1")]
        excluded = [c.getPath() for c in self.catres if c.getPath() == "/plone/my_doc1"]
        map(lambda l:l.sort(), [catpaths, filtered, excluded])
        self.assertTrue(type(filtered) in [ListType, TupleType],
            'Object type, returned by filteredOut method of "%s" utility '\
            'not list nor tuple' % pathfname)
        self.assertTrue(set(catpaths)-set(filtered) == set(excluded),
            'Wrong filtered-out by "%s" filter:\nsrc %s\nres %s\nexcluded %s' % (
             pathfname, catpaths, filtered, excluded))
        
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBOFilterUtilities))
    suite.addTest(makeSuite(TestDefaultFilters))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
#    framework()
