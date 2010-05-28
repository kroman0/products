from base import *
from DateTime import DateTime

from zope.component import getSiteManager, getGlobalSiteManager
from archetypes.schemaextender.interfaces import ISchemaExtender

from Products.CMFPlone.utils import _createObjectByType

class TestNewsSitemapsXML(FunctionalTestCase):

    def afterSetUp(self):
        super(TestNewsSitemapsXML, self).afterSetUp()
        # Create news sitemaps
        _createObjectByType("Sitemap", self.portal, id="news-sitemaps",
                            sitemapType="news", portalTypes=("News Item",))
        self.portal["news-sitemaps"].at_post_create_script()
        # Add testing news item to portal
        self.pubdate = (DateTime()+1).strftime("%Y-%m-%d")
        my_news = self.portal.invokeFactory("News Item", id="my_news")
        self.my_news = self.portal["my_news"]
        self.my_news.edit(text="Test news item", title="First news (test)", language="ua",
                          effectiveDate=self.pubdate)
        self.portal.portal_workflow.doActionFor(self.my_news, "publish")
        self.reParse()

    def reParse(self):
        # Parse news sitemap
        self.sitemap = self.publish("/"+self.portal.absolute_url(1) + "/news-sitemaps",
                                    "%s:%s" % (portal_owner, default_password)).getBody()
        parsed_sitemap = parse(self.sitemap)
        self.start = parsed_sitemap["start"]
        self.data = parsed_sitemap["data"]

    def test_urlset(self):
        self.assert_("urlset" in self.start.keys())
        urlset = self.start["urlset"]
        self.assertEqual(urlset.get("xmlns", ""), "http://www.sitemaps.org/schemas/sitemap/0.9")
        self.assertEqual(urlset.get("xmlns:n", ""), "http://www.google.com/schemas/sitemap-news/0.9")

    def test_url(self):
        self.assert_("url" in self.start.keys())

    def test_loc(self):
        self.assert_("loc" in self.start.keys())
        self.assert_(self.portal.absolute_url() + "/my_news" in self.data)

    def test_nnews(self):
        self.assert_("n:news" in self.start.keys())
        
    def test_npublication(self):
        self.assert_("n:publication" in self.start.keys())
        self.assert_("n:name" in self.start.keys())
        self.assert_("First news" in self.data, "No 'First news' in data")
        self.assert_("n:language" in self.start.keys())
        self.assert_("ua" in self.data, "No 'ua' in data")

    def test_npublication_date(self):
        self.assert_("n:publication_date" in self.start.keys())
        self.assert_(self.pubdate in self.data, "No %s in data" % self.pubdate)
        
    def test_ntitle(self):
        self.assert_("n:title" in self.start.keys())
        self.assert_("First news (test)" in self.data, "No 'First news (test)' in data")

    def test_no_naccess(self):
        self.assert_("n:access" not in self.start.keys())

    def test_no_ngenres(self):
        self.assert_("n:genres" not in self.start.keys())

    def test_naccess(self):
        # Test when access present
        self.my_news._setProperty("gsm_access", "Registration")
        self.my_news.reindexObject()
        self.reParse()
        self.assert_("n:access" in self.start.keys())
        self.assert_("Registration" in self.data, "No 'Registration' in data")

    def test_ngenres(self):
        # Test when genres present
        self.my_news._setProperty("gsm_genres", "PressRelease")
        self.my_news.reindexObject()
        self.reParse()
        self.assert_("n:genres" in self.start.keys())
        self.assert_("PressRelease" in self.data, "No 'PressRelease' in data")


from Products.ATContentTypes.interface import IATNewsItem
from quintagroup.plonegooglesitemaps.content.newsextender import NewsExtender
from quintagroup.plonegooglesitemaps.utils import addLocalSchemaExtenderAdapter
from quintagroup.plonegooglesitemaps.utils import removeLocalSchemaExtenderAdapter

class TestDynamicSchemaExtending(TestCase):

    def afterSetUp(self):
        super(TestDynamicSchemaExtending, self).afterSetUp()
        self.loginAsPortalOwner()
        # Add testing news item to portal
        my_news = self.portal.invokeFactory("News Item", id="my_news")
        self.my_news = self.portal["my_news"]
        my_doc = self.portal.invokeFactory("Document", id="my_doc")
        self.my_doc = self.portal["my_doc"]

    def testNotExtendByDefault(self):
        # Neither of object has extended fields
        self.assertEqual(self.my_news.getField("gsm_access"), None)
        self.assertEqual(self.my_news.getField("gsm_genres"), None)
        self.assertEqual(self.my_doc.getField("gsm_access"), None)
        self.assertEqual(self.my_doc.getField("gsm_genres"), None)
    
    def testExtend(self):
        addLocalSchemaExtenderAdapter(self.portal, IATNewsItem)
        self.assertNotEqual(self.my_news.getField("gsm_access"), None)
        self.assertNotEqual(self.my_news.getField("gsm_genres"), None)
        # But for document schema should not extended
        self.assertEqual(self.my_doc.getField("gsm_access"), None)
        self.assertEqual(self.my_doc.getField("gsm_genres"), None)

    def testRemoveExtend(self):
        addLocalSchemaExtenderAdapter(self.portal, IATNewsItem)
        self.assertNotEqual(self.my_news.getField("gsm_access"), None)
        self.assertNotEqual(self.my_news.getField("gsm_genres"), None)
        removeLocalSchemaExtenderAdapter(self.portal, IATNewsItem)
        self.assertEqual(self.my_news.getField("gsm_access"), None)
        self.assertEqual(self.my_news.getField("gsm_genres"), None)

    def testRegistrationOnLocalSM(self):
        """SchemaExtender adapters must be registered
           in Local SiteManager only.
        """
        localsm = getSiteManager(self.portal)
        globalsm = getGlobalSiteManager()
        # Check if by default neither site manger
        # has ISchemaExtender adapter registered in.
        self.assertNotEqual(localsm, globalsm)
        self.assertEqual(localsm.queryAdapter(self.my_news, ISchemaExtender), None)
        self.assertEqual(globalsm.queryAdapter(self.my_news, ISchemaExtender), None)
        # Now register SchemaExtender adapter and
        # check if it present in Local SiteManger only
        addLocalSchemaExtenderAdapter(self.portal, IATNewsItem)
        self.assertNotEqual(localsm.queryAdapter(self.my_news, ISchemaExtender), None)
        self.assertEqual(globalsm.queryAdapter(self.my_news, ISchemaExtender), None)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNewsSitemapsXML))
    suite.addTest(makeSuite(TestDynamicSchemaExtending))
    return suite
