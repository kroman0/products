#
# Tests related to general Sitemap type.
#
from base import *
from Products.CMFPlone.utils import _createObjectByType


class TestSitemapType(FunctionalTestCase):

    def afterSetUp(self):
        super(TestSitemapType, self).afterSetUp()
        self.auth = 'admin:admin'
        self.contentSM = _createObjectByType('Sitemap', self.portal, id='google-sitemaps')
        self.portal.portal_membership.addMember('admin', 'admin', ('Manager',), [])

    def testFields(self):
        field_ids = map(lambda x:x.getName(), self.contentSM.Schema().fields())
        # test old Sitemap settings fields
        self.assert_('id' in field_ids)
        self.assert_('portalTypes' in field_ids)
        self.assert_('states' in field_ids)
        self.assert_('blackout_list' in field_ids)
        self.assert_('urls' in field_ids)
        self.assert_('pingTransitions' in field_ids)
        # test new sitemap type field
        self.assert_('sitemapType' in field_ids)

    def testSitemapTypes(self):
        sitemap_types = self.contentSM.getField('sitemapType').Vocabulary().keys()
        self.assert_('content' in sitemap_types)
        self.assert_('mobile' in sitemap_types)
        self.assert_('news' in sitemap_types)

    def testAutoSetLayout(self):
        response = self.publish('/%s/createObject?type_name=Sitemap' % \
                                self.portal.absolute_url(1), basic=self.auth)
        location = response.getHeader('location')
        newurl = location[location.find('/'+self.portal.absolute_url(1)):]

        msm_id = 'mobile_sitemap'
        form = {'id': msm_id,
                'sitemapType':'mobile',
                'portalTypes':['Document',],
                'states':['published'],
                'form_submit':'Save',
                'form.submitted':1,
                }
        post_data = StringIO(urlencode(form))
        response = self.publish(newurl, request_method='POST', stdin=post_data, basic=self.auth)
        msitemap = getattr(self.portal, msm_id)

        self.assertEqual(msitemap.defaultView(), 'mobile-sitemap.xml')

    def txestPingSetting(self):
        pwf = self.portal.portal_workflow['plone_workflow']
        self.assertEqual(self.contentSM.getPingTransitions(), ())

        self.contentSM.setPingTransitions(('plone_workflow#publish',))
        self.assertEqual(self.contentSM.getPingTransitions(), ('plone_workflow#publish',))
        self.assert_(ping_googlesitemap in pwf.scripts.keys(),"Not add wf script")


class TestSettings(FunctionalTestCase):

    def afterSetUp(self):
        super(TestSettings, self).afterSetUp()

        self.workflow = self.portal.portal_workflow
        self.gsm_props = self.portal.portal_properties['googlesitemap_properties']
        self.auth = 'admin:admin'
        self.contentSM = _createObjectByType('Sitemap', self.portal, id='google-sitemaps')

        self.sitemapUrl = '/'+self.portal.absolute_url(1) + '/google-sitemaps'

        self.portal.portal_membership.addMember('admin', 'admin', ('Manager',), [])

        # Add testing document to portal
        my_doc = self.portal.invokeFactory('Document', id='my_doc')
        self.my_doc = self.portal['my_doc']
        self.my_doc.edit(text_format='plain', text='hello world')
        self.my_doc_url = self.my_doc.absolute_url()

    def testMetaTypeToDig(self):
        self.workflow.doActionFor(self.my_doc, 'publish')
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.my_doc_url))

        self.contentSM.setPortalTypes([])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(not hasURL(sitemap, self.my_doc_url))

        self.contentSM.setPortalTypes(['Document'])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.my_doc_url))

    def testStates(self):
        self.workflow.doActionFor(self.my_doc, 'publish')
        self.contentSM.setStates(['visible'])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(not hasURL(sitemap, self.my_doc_url))

        self.contentSM.setStates(['published'])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.my_doc_url))

    def test_blackout_entries(self):
        self.workflow.doActionFor(self.my_doc, 'publish')
        self.contentSM.setBlackout_list((self.my_doc.getId(),))

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(not hasURL(sitemap, self.my_doc_url))

        self.contentSM.setBlackout_list([])
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.my_doc_url))

    def test_regexp(self):
        self.workflow.doActionFor(self.my_doc, 'publish')
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(not hasURL(sitemap, self.portal.absolute_url()))

        regexp = "s/\/%s//"%self.my_doc.getId()
        self.contentSM.setReg_exp([regexp])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.portal.absolute_url()))

    def test_add_urls(self):
        self.contentSM.setUrls(['http://w1', 'w2', '/w3'])
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
    suite.addTest(makeSuite(TestSitemapType))
    suite.addTest(makeSuite(TestSettings))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
#    framework()
