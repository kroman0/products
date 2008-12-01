#
# Tests for qPloneGoogleSitemaps
#

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase
from XMLParser import parse, hasURL
import Products.qPloneGoogleSitemaps

PRODUCT = 'qPloneGoogleSitemaps'
PRODUCTS = (PRODUCT,)

# Import configure.zcml for qPloneGoogleSitemaps
fiveconfigure.debug_mode = True
zcml.load_config('configure.zcml', Products.qPloneGoogleSitemaps)
fiveconfigure.debug_mode = False

PloneTestCase.installProduct(PRODUCT)
PloneTestCase.setupPloneSite(extension_profiles=("Products.%s:default" % PRODUCT,))

class TestqPloneGoogleSitemapsInstallation(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def testType(self):
        pt = self.portal.portal_types
        self.assert_('Sitemap' in pt.objectIds(), 
            'No "Sitemap" type after installation')
        #Test views
        views = pt.getTypeInfo('Sitemap').view_methods
        self.assert_('sitemap.xml' in views, 
            'No "sitemap.xml" view for Sitemap type')
        self.assert_('mobile-sitemap.xml' in views, 
            'No "mobile-sitemap.xml" view for Sitemap type')
        self.assert_('news-sitemap.xml' in views, 
            'No "news-sitemap.xml" view for Sitemap type')

    def testGSMProperties(self):
        pp = self.portal.portal_properties

        # Test types_not_searched
        self.assert_("Sitemap" in pp['site_properties'].getProperty('types_not_searched'), 
            'No "Sitemap" added to types not searched on installation')
        # Test metaTypesNotToList
        self.assert_("Sitemap" in pp['navtree_properties'].getProperty('metaTypesNotToList'), 
            'No "Sitemap" added to types not to list on installation')

        # Test 'googlesitemap_properties'
        self.assert_('googlesitemap_properties' in pp.objectIds(), 
            'No "googlesitemap_properties" after installation')
        qsmprops = pp['googlesitemap_properties']
        self.assert_(qsmprops.hasProperty('content_default'),
            'No "content_default" property added on installation')
        self.assert_(qsmprops.hasProperty('mobile_default'),
            'No "mobile_default" property added on installation')
        self.assert_(qsmprops.hasProperty('news_default'),
            'No "news_default" property added on installation')
        self.assert_(qsmprops.hasProperty('verification_filename'),
            'No "verification_filename" property added on installation')

    def testGSMProperties(self):
        pp = self.portal.portal_properties

        self.assert_('googlesitemap_properties' in pp.objectIds(), 
            'No "googlesitemap_properties" after installation')
        qsmprops = pp['googlesitemap_properties']
        self.assert_(qsmprops.hasProperty('content_default'),
            'No "content_default" property added on installation')
        self.assert_(qsmprops.hasProperty('mobile_default'),
            'No "mobile_default" property added on installation')
        self.assert_(qsmprops.hasProperty('news_default'),
            'No "news_default" property added on installation')
        self.assert_(qsmprops.hasProperty('verification_filename'),
            'No "verification_filename" property added on installation')

    def testSkins(self):
        ps = self.portal.portal_skins
        self.assert_('qPloneGoogleSitemaps' in ps.objectIds(), 
            'No "qPloneGoogleSitemaps" skin layer in portal_skins')
        self.assert_('qPloneGoogleSitemaps' in ps.getSkinPath(ps.getDefaultSkin()),
            'No "qPloneGoogleSitemaps" skin layer in default skin')

    def testConfiglet(self):
        cp = self.portal.portal_controlpanel
        self.assert_([1 for ai in cp.listActionInfos() if ai['id']=='qPloneGoogleSitemaps'], 
            'No "qPloneGoogleSitemaps" configlet added to plone control panel')

    def testCatalog(self):
        catalog = self.portal.portal_catalog
        self.assert_('hasMobileContent' in catalog.indexes(),
            'No "hasMobileContent" index in portal_catalog')



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

        regexp = "s/\/%s//"%self.my_doc.getId()
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
    suite.addTest(makeSuite(TestqPloneGoogleSitemapsInstallation))
    #suite.addTest(makeSuite(TestqPloneGoogleSitemaps))
    #suite.addTest(makeSuite(TestSettings))
    return suite

if __name__ == '__main__':
    framework()
