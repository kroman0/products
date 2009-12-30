import unittest
import os.path

import transaction

from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from collective.transmogrifier.interfaces import ITransmogrifier

ztc.installProduct('Quills')
ztc.installProduct('fatsyndication')

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import Products.Five
    zcml.load_config('configure.zcml', Products.Five)
    import quintagroup.transmogrify.simpleblog2quills
    zcml.load_config('configure.zcml', quintagroup.transmogrify.simpleblog2quills)
    import quintagroup.transmogrify.simpleblog2quills.tests
    zcml.load_config('test_import.zcml', quintagroup.transmogrify.simpleblog2quills.tests)
    # this is needed because 'importStep' unknown directive error is raised somewhere
    import Products.GenericSetup
    zcml.load_config('meta.zcml', Products.GenericSetup)
    import Products.Quills
    zcml.load_config('configure.zcml', Products.Quills)
    fiveconfigure.debug_mode = False

setup_product()
ptc.setupPloneSite(products=['Quills'])

class TestImport(ptc.PloneTestCase):
    """ Test importing of PloneFormGen content.
    """

    def afterSetUp(self):
        self.addProduct('Quills')
        if 'blog' not in self.portal:
            # run transmogrifier pipeline
            transmogrifier = ITransmogrifier(self.portal)
            transmogrifier('test_import')

    def beforeTearDown(self):
        transaction.commit()

    def test_site_structure(self):
        self.failIf('blog' not in self.portal)
        self.failIf('root-entry' not in self.portal.blog)
        self.failIf('folder' not in self.portal.blog)
        self.failIf('folder-entry' not in self.portal.blog.folder)

    def test_blog(self):
        blog = self.portal['blog']

        self.assertEqual(blog.getPortalTypeName(), 'Weblog')
        self.assertEqual(blog['title'], 'Test Blog')
        self.assertEqual(blog.Description(), 'This is test blog.')

    def test_blog_entry(self):
        entry = self.portal['blog']['root-entry']

        self.assertEqual(entry.getPortalTypeName(), 'WeblogEntry')
        self.assertEqual(entry['title'], 'Root entry')
        self.assertEqual(entry.Description(), 'This entry was created in root of blog.')
        self.assertEqual(entry.getText(), '<p>We are testing importing of blog entry.</p>')
        self.assertEqual(entry.Subject(), ('Plone', 'Zope'))
        self.assertEqual(entry.modified().HTML4(), '2007-11-14T10:32:11Z')
        # now workflow of WeblogEntry is assumed to be 'plone_workflow'
        # but it must be configured in type configuration
        self.failIf('plone_workflow' not in entry.workflow_history)

    def test_blog_folder(self):
        folder = self.portal['blog']['folder']

        self.assertEqual(folder.getPortalTypeName(), 'Folder')
        self.assertEqual(folder['title'], 'Blog folder')
        self.assertEqual(folder.Description(), 'Folder in blog.')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestImport))
    return suite
