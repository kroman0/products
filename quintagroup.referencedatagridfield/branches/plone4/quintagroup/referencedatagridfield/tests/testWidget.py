import re
import unittest

from Products.PloneTestCase.PloneTestCase import portal_owner
from Products.PloneTestCase.PloneTestCase import default_password

from quintagroup.referencedatagridfield.tests.base import FunctionalTestCase
from quintagroup.referencedatagridfield import ReferenceDataGridWidget


class TestWidgetView(FunctionalTestCase):
    """ ReferenceDataGridWidget unit tests """

    def afterSetUp(self):
        self.loginAsPortalOwner()
        # Prevent section links
        sp = self.portal.portal_properties.site_properties
        sp._updateProperty("disable_nonfolderish_sections", True)
        # Prepare testing data and data for functional test
        self.createDemo(wfaction="publish")
        self.demo_path = "/" + self.demo.absolute_url(1)
        self.basic_auth = ':'.join((portal_owner,default_password))
        # Regexp for getting links
        self.relink = re.compile("<a\s+[^>]*?href=\"(.*?)\"[^>]*?>\s*(.*?)\s*</a>",
                                 re.I|re.S|re.M)

    def test_LinkDefaultTitle(self):
        self.demo.edit(demo_rdgf=[{"link": "http://google.com"}])
        html = self.publish(self.demo_path, self.basic_auth).getBody()
        links = dict(self.relink.findall(html))
        
        self.assertEqual(links.has_key("http://google.com"), True)
        self.assertEqual("http://google.com" in links["http://google.com"], True)
 
    def test_LinkCustomTitle(self):
        self.demo.edit(demo_rdgf=[{"link": "http://google.com", "title": "Google"}])
        html = self.publish(self.demo_path, self.basic_auth).getBody()
        links = dict(self.relink.findall(html))
        
        self.assertEqual(links.has_key("http://google.com"), True)
        self.assertEqual("Google" in links["http://google.com"], True)
 
    def test_UIDDefaultTitle(self):
        data = [{"uid": self.doc.UID(), "link": self.doc.absolute_url(1)}]
        self.demo.edit(demo_rdgf=data)
        html = self.publish(self.demo_path, self.basic_auth).getBody()
        links = dict(self.relink.findall(html))

        doc_url = self.doc.absolute_url()
        doc_title = self.doc.Title()
        self.assertEqual(links.has_key(doc_url), True)
        self.assertEqual(doc_title in links[doc_url], True)

    def test_UIDCustomTitle(self):
        data = [{"uid": self.doc.UID(), "link": self.doc.absolute_url(1),
                 "title": "Custom Title"},]
        self.demo.edit(demo_rdgf=data)
        html = self.publish(self.demo_path, self.basic_auth).getBody()
        links = dict(self.relink.findall(html))

        doc_url = self.doc.absolute_url()
        self.assertEqual(links.has_key(doc_url), True)
        self.assertEqual("Custom Title" in links[doc_url], True)

    def test_LinksOrder(self):
        relink = re.compile("<a\s+[^>]*?href=\"(.*?)\"[^>]*?>", re.I|re.S)
        data = [{"link": "http://google.com"},
                {"uid": self.doc.UID(), "link": self.doc.absolute_url(1)}]
        # First check in one order
        self.demo.edit(demo_rdgf=data)
        html = self.publish(self.demo_path, self.basic_auth).getBody()
        links = relink.findall(html)
        idx1 = links.index("http://google.com")
        idx2 = links.index(self.doc.absolute_url())
        self.assertEqual( idx1 < idx2, True)
        # Now reverse rows order
        data.reverse()
        self.demo.edit(demo_rdgf=data)
        html = self.publish(self.demo_path, self.basic_auth).getBody()
        links = relink.findall(html)
        idx1 = links.index("http://google.com")
        idx2 = links.index(self.doc.absolute_url())
        self.assertEqual( idx1 > idx2, True)
        

def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestWidgetView),
        #unittest.makeSuite(TestWidgetEdit),
        ])
