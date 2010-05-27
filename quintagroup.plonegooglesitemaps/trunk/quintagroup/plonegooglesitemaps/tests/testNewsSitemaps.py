from base import *
from Products.CMFPlone.utils import _createObjectByType
from DateTime import DateTime

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
        my_news = self.portal["my_news"]
        my_news.edit(text="Test news item", title="First news (test)", language="ua",
                     effectiveDate=self.pubdate)
        
        self.portal.portal_workflow.doActionFor(my_news, "publish")
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

    def test_naccess(self):
        pass

    def test_ngenres(self):
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNewsSitemapsXML))
    return suite
