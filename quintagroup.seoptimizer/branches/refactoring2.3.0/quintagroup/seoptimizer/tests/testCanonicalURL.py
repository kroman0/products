import re
from zope.component import queryAdapter
from zope.component import provideAdapter
from plone.indexer.decorator import indexer

try:
    from plone.indexer.decorator import indexer
except ImportError:
    IS_NEW = False
    from Products.CMFPlone.CatalogTool import registerIndexableAttribute
else:
    IS_NEW = True

from Products.CMFCore.interfaces import IContentish
from Products.Archetypes.interfaces import IBaseContent

from quintagroup.canonicalpath.interfaces import ICanonicalPath
from quintagroup.seoptimizer.interfaces import ISEOCanonicalPath
from base import *

class TestCanonicalURL(FunctionalTestCase):

    def afterSetUp(self):
        self.basic_auth = ':'.join((portal_owner,default_password))
        self.loginAsPortalOwner()
        # Preparation for functional testing
        self.portal.invokeFactory('Document', id='mydoc')
        self.mydoc = self.portal['mydoc']
        self.mydoc_path = "/%s" % self.mydoc.absolute_url(1)
        self.curl = re.compile('<link\srel\s*=\s*"canonical"\s+' \
            '[^>]*href\s*=\s*\"([^\"]*)\"[^>]*>', re.S|re.M)


    def test_CanonicalURL(self):
        html = self.publish(self.mydoc_path, self.basic_auth).getBody()
        foundcurls = self.curl.findall(html)
        mydoc_url = self.mydoc.absolute_url()

        self.assertTrue([1 for curl in foundcurls if curl==mydoc_url],
           "Wrong CANONICAL URL for document: %s, all must be: %s" % (
           foundcurls, mydoc_url))

    def test_updateCanonicalURL(self):
        mydoc_url_new = self.mydoc.absolute_url() + '.new'
        # Update canonical url property
        self.publish(self.mydoc_path + '/@@seo-context-properties?' \
           'seo_canonical_override=checked&seo_canonical=%s&' \
           'form.submitted=1' % mydoc_url_new, self.basic_auth)
        # Test updated canonical url
        html = self.publish(self.mydoc_path, self.basic_auth).getBody()
        foundcurls = self.curl.findall(html)

        qseo_url = self.mydoc.getProperty('qSEO_canonical','')
        self.assertTrue(qseo_url == mydoc_url_new,
           "Not set 'qSEO_canonical' property")
        self.assertTrue([1 for curl in foundcurls if curl==mydoc_url_new],
           "Wrong CANONICAL URL for document: %s, all must be: %s" % (
           foundcurls, mydoc_url_new))

    def test_SEOCanonicalAdapterRegistration(self):
        portal_seocanonical = queryAdapter(self.portal, interface=ISEOCanonicalPath)
        self.assertTrue(portal_seocanonical is not None,
            "Not registered ISEOCanonicalPath adapter")

        mydoc_seocanonical = queryAdapter(self.mydoc, interface=ISEOCanonicalPath)
        self.assertTrue(mydoc_seocanonical is not None,
            "Not registered ISEOCanonicalPath adapter")

    def test_canonicalAdapterRegistration(self):
        canonical_portal = queryAdapter(self.portal, interface=ICanonicalPath)
        self.assertTrue(canonical_portal is not None,
            "Not registered ICanonicalPath adapter for portal root")

        canonical_mydoc = queryAdapter(self.mydoc, interface=ICanonicalPath)
        self.assertTrue(canonical_mydoc is not None,
            "Not registered ICanonicalPath adapter for the documnent")

    def test_canonicalAdapter(self):
        purl = getToolByName(self.portal, 'portal_url')
        mydoc_path_rel = '/'+'/'.join(purl.getRelativeContentPath(self.mydoc))

        canonical = queryAdapter(self.mydoc, ISEOCanonicalPath)
        cpath = canonical.canonical_path()
        self.assertTrue(cpath == mydoc_path_rel,
            "By canonical path adapter got: '%s', must be: '%s'" % (
             cpath, mydoc_path_rel))

        # Update canonical url property
        mydoc_url_new = self.mydoc.absolute_url() + '.new'
        self.publish(self.mydoc_path + '/@@seo-context-properties?' \
            'seo_canonical_override=checked&seo_canonical=%s' \
            '&form.submitted=1' % mydoc_url_new, self.basic_auth)

        mydoc_path_rel_new = mydoc_path_rel + '.new'
        newcpath = canonical.canonical_path()
        self.assertTrue(newcpath == mydoc_path_rel_new,
            "By canonical path adapter got: '%s', must be: '%s'" % (
             newcpath, mydoc_path_rel_new))


    def addIndexerOld(self):
        def canonical_path(obj, **kwargs):
            """Return canonical_path property for the object.
            """
            cpath = queryAdapter(obj, interface=ISEOCanonicalPath)
            if cpath:
                return cpath.canonical_path()
            return None
        registerIndexableAttribute("canonical_path", test_column)

    def addIndexerNew(self):
        @indexer(IContentish)
        def canonical_path(obj, **kwargs):
            """Return canonical_path property for the object.
            """
            cpath = queryAdapter(obj, interface=ISEOCanonicalPath)
            if cpath:
                return cpath.canonical_path()
            return None

        provideAdapter(canonical_path, name='canonical_path')

    def testCatalogUpdated(self):
        purl = getToolByName(self.portal, 'portal_url')
        catalog = getToolByName(self.portal, 'portal_catalog')
        if IS_NEW:
            self.addIndexerNew()
        else:
            self.addIndexerOld()
        catalog.addColumn('canonical_path')

        canonical = queryAdapter(self.mydoc, ISEOCanonicalPath)
        cpath = canonical.canonical_path()

        # get catalog data before update
        mydoc_catalog_canonical = catalog(id="mydoc")[0].canonical_path
        self.assertTrue(not mydoc_catalog_canonical)

        # Update canonical url property
        mydoc_url_new = self.mydoc.absolute_url() + '.new'
        self.publish(self.mydoc_path + '/@@seo-context-properties?' \
            'seo_canonical_override=checked&seo_canonical=%s' \
            '&form.submitted=1' % mydoc_url_new, self.basic_auth)

        newcpath = canonical.canonical_path()
        mydoc_catalog_canonical = catalog(id="mydoc")[0].canonical_path
        self.assertTrue(newcpath == mydoc_catalog_canonical,
            "canonical path get by adapter: '%s' not equals to cataloged one: '%s'" % (
             newcpath, mydoc_catalog_canonical))


    def testSEOCanonicalAdapter4OFSFolder(self):
        atct_tool = self.portal.portal_atct
        seocan = queryAdapter(self.mydoc, ISEOCanonicalPath)
        self.assertTrue(seocan is not None,
            "seo canonical adapter not found for 'ATCT Tool'")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCanonicalURL))
    return suite
