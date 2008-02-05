#
# Tests for qPloneGoogleSitemaps
#
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from XMLParser import parse, hasURL

PRODUCT = 'qPloneGoogleSitemaps'
PRODUCTS = (PRODUCT,)
PloneTestCase.installProduct(PRODUCT)
PloneTestCase.setupPloneSite(products = PRODUCTS)

class TestqPloneGoogleSitemaps(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

        self.membership = self.portal.portal_membership
        self.workflow = self.portal.portal_workflow
        self.auth = 'admin:admin'
        self.sitemapUrl = '/'+self.portal.absolute_url(1) + '/google-sitemaps'
        self.membership.addMember('admin', 'admin', ('Manager',), [])

        # Add testing document to portal
        my_doc = self.portal.invokeFactory('Document', id='my_doc')
        self.my_doc = self.portal['my_doc']
        self.my_doc.edit(text_format='plain', text='hello world')

    def testInstallation(self):
        installed = self.portal.portal_quickinstaller.isProductInstalled(PRODUCT)
        self.assert_(installed, 'Product not installed')

    def testSitemap(self):
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        parsed_sitemap = parse(sitemap)
        start = parsed_sitemap['start']
        data = parsed_sitemap['data']
        self.assertEqual(len(start.keys()), 1)
        self.assert_('urlset' in start.keys())

        self.workflow.doActionFor(self.my_doc, 'publish')

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        parsed_sitemap = parse(sitemap)
        start = parsed_sitemap['start']
        data = parsed_sitemap['data']
        self.assertEqual(len(start.keys()), 4)
        self.assert_('urlset' in start.keys())
        self.assert_('url' in start.keys())
        self.assert_('loc' in start.keys())
        self.assert_('lastmod' in start.keys())

        self.assert_(data[0] == self.my_doc.absolute_url(0), 'Incorect url')

    def testVerificationFile(self):
        self.portal.gsm_create_verify_file('verif_file')
        vf_created = hasattr(self.portal, 'verif_file')
        self.assert_(vf_created, 'Verification file not created')

        self.portal.gsm_delete_verify_file()
        vf_created = hasattr(self.portal, 'verif_file')
        self.assert_(not vf_created, 'Verification file not removed')

class TestSettings(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

        self.membership = self.portal.portal_membership
        self.workflow = self.portal.portal_workflow
        self.gsm_props = self.portal.portal_properties['googlesitemap_properties']
        self.auth = 'admin:admin'
        self.sitemapUrl = '/'+self.portal.absolute_url(1) + '/google-sitemaps'

        self.membership.addMember('admin', 'admin', ('Manager',), [])

        # Add testing document to portal
        my_doc = self.portal.invokeFactory('Document', id='my_doc')
        self.my_doc = self.portal['my_doc']
        self.my_doc.edit(text_format='plain', text='hello world')
        self.my_doc_url = self.my_doc.absolute_url()

    def testMetaTypeToDig(self):
        self.workflow.doActionFor(self.my_doc, 'publish')
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.my_doc_url))

        self.gsm_props.manage_changeProperties(portalTypes = [])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(not hasURL(sitemap, self.my_doc_url))

        self.gsm_props.manage_changeProperties(portalTypes = ['Document'])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.my_doc_url))

    def testStates(self):
        self.workflow.doActionFor(self.my_doc, 'publish')
        self.gsm_props.manage_changeProperties(states = ['visible'])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(not hasURL(sitemap, self.my_doc_url))

        self.gsm_props.manage_changeProperties(states = ['published'])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.my_doc_url))

    def test_blackout_entries(self):
        self.workflow.doActionFor(self.my_doc, 'publish')
        self.gsm_props.manage_changeProperties(blackout_list = (self.my_doc.getId(),))
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(not hasURL(sitemap, self.my_doc_url))

        self.gsm_props.manage_changeProperties(blackout_list = [])
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.my_doc_url))

    def test_regexp(self):
        self.workflow.doActionFor(self.my_doc, 'publish')
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(not hasURL(sitemap, self.portal.absolute_url()))

        regexp = 's//%s//'%self.my_doc.getId()
        self.gsm_props.manage_changeProperties(reg_exp = [regexp])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.portal.absolute_url()))

    def test_add_urls(self):
        self.gsm_props.manage_changeProperties(urls = ['http://w1', 'w2', '/w3'])
        w1_url = 'http://w1'
        w2_url = self.portal.absolute_url() + '/w2'
        w3_url = self.portal.getPhysicalRoot().absolute_url() + '/w3'
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()

        self.assert_(hasURL(sitemap, w1_url))
        self.assert_(hasURL(sitemap, w2_url))
        self.assert_(hasURL(sitemap, w3_url))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestqPloneGoogleSitemaps))
    suite.addTest(makeSuite(TestSettings))
    return suite

if __name__ == '__main__':
    framework()
