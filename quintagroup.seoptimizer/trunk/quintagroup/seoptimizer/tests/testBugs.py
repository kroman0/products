import urllib
from cStringIO import StringIO

from OFS.interfaces import ITraversable

from zope.component import providedBy
from zope.component import getGlobalSiteManager
from zope.component import queryAdapter, getMultiAdapter
from zope.interface import directlyProvides
from zope.viewlet.interfaces import IViewlet, IViewletManager
from zope.publisher.browser import TestRequest

from quintagroup.seoptimizer.browser.interfaces import IPloneSEOLayer
from quintagroup.canonicalpath.interfaces import ICanonicalLink
from quintagroup.canonicalpath.adapters import DefaultCanonicalLinkAdapter
from base import *


class TestBugs(FunctionalTestCase):

    def afterSetUp(self):
        self.basic_auth = ':'.join((portal_owner,default_password))
        self.loginAsPortalOwner()
        # prepare test document
        my_doc = self.portal.invokeFactory('Document', id='my_doc')
        self.my_doc = self.portal['my_doc']
        self.mydoc_path = "/%s" % self.my_doc.absolute_url(1)

    def test_modification_date(self):
        """ Modification date changing on SEO properties edit """
        form_data = {'seo_title': 'New Title',
                     'seo_title_override:int': 1,
                     'form.submitted:int': 1}

        md_before = self.my_doc.modification_date
        self.publish(path=self.mydoc_path+'/@@seo-context-properties',
                     basic=self.basic_auth, request_method='POST',
                     stdin=StringIO(urllib.urlencode(form_data)))
        md_after = self.my_doc.modification_date

        self.assertNotEqual(md_before, md_after)

    def test_bug_20_at_plone_org(self):
        portal = self.portal
        fp = portal['front-page']
        request = portal.REQUEST
        view = portal.restrictedTraverse('@@plone')

        manager = getMultiAdapter((fp, request, view), IViewletManager,
                        name=u'plone.htmlhead')
        viewlet = getMultiAdapter((fp, request, view, manager), IViewlet,
                        name=u'plone.htmlhead.title')
        viewlet.update()
        old_title = viewlet.render()

        # add IPloneSEOLayer
        directlyProvides(request, IPloneSEOLayer)

        viewlet = getMultiAdapter((fp, request, view, manager), IViewlet,
                        name=u'plone.htmlhead.title')
        viewlet.update()
        new_title = viewlet.render()

        self.assertEqual(old_title, new_title)

    def test_bug_22_at_plone_org(self):
        """If ICanonicalLink adapter is not found for the context object
           page rendering should not break, but only canonical link
           should disappear.
        """
        curl = re.compile('<link\srel\s*=\s*"canonical"\s+' \
                         '[^>]*href\s*=\s*\"([^\"]*)\"[^>]*>', re.S|re.M)
        # When adapter registered for the object - canoncal link present on the page
        self.assertNotEqual( queryAdapter(self.my_doc, ICanonicalLink), None)

        res = self.publish(path=self.mydoc_path, basic=self.basic_auth)
        self.assertNotEqual(curl.search(res.getBody()), None)

        # Now remove adapter from the registry -> this should :
        #     - not break page on rendering;
        #     - canonical link will be absent on the page
        gsm = getGlobalSiteManager()
        gsm.unregisterAdapter(DefaultCanonicalLinkAdapter, [ITraversable,],
                              ICanonicalLink)
        self.assertEqual( queryAdapter(self.my_doc, ICanonicalLink), None)

        res = self.publish(path=self.mydoc_path, basic=self.basic_auth)
        self.assertEqual(curl.search(res.getBody()), None)

        # register adapter back in the global site manager
        gsm.registerAdapter(DefaultCanonicalLinkAdapter, [ITraversable,],
                            ICanonicalLink)
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBugs))
    return suite
