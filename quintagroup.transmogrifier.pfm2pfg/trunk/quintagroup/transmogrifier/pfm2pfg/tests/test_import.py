import unittest
import os.path

from zope.interface import classProvides, implements

from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from collective.transmogrifier.interfaces import ISectionBlueprint, ISection, ITransmogrifier

class Source(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous

    def __iter__(self):
        for item in self.previous:
            yield item

        fname = os.path.join(os.path.dirname(__file__), 'post-software.xml')
        xml = file(fname).read()
        item = dict(
            _type='PloneFormMailer',
            _path='post-software',
            _files=dict(
                marshall=dict(
                    name='.marshall.xml',
                    data=xml
                )
            )
        )
        yield item

ztc.installProduct('PloneFormGen')

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import quintagroup.transmogrifier.pfm2pfg
    zcml.load_config('configure.zcml', quintagroup.transmogrifier.pfm2pfg)
    import quintagroup.transmogrifier.pfm2pfg.tests
    zcml.load_config('test_import.zcml', quintagroup.transmogrifier.pfm2pfg.tests)
    fiveconfigure.debug_mode = False

setup_product()
ptc.setupPloneSite(products=['PloneFormGen'])

class TestImport(ptc.PloneTestCase):
    """ Test importing of PloneFormGen content.
    """

    def afterSetUp(self):
        # run transmogrifier pipeline
        transmogrifier = ITransmogrifier(self.portal)
        transmogrifier('test_import')

    def test_form_folder(self):
        self.failUnless('post-software' in self.portal)
        form = self.portal['post-software']

        self.assertEqual(form['title'], 'Publish new content management product or module')
        self.assertEqual(form.getFormPrologue(), '<p>form prologue</p>')
        self.assertEqual(form.getFormEpilogue(), '<p>form epilogue</p>')
        #self.assertEqual(form['thanksPageOverride'], 'string:')
        #self.assertEqual(form['afterValidationOverride'], 'redirect_to:')

    def test_mailer(self):
        form = self.portal['post-software']
        self.failUnless('mailer' in form)
        mailer = form['mailer']
        #import pdb; pdb.set_trace()

        self.assertEqual(mailer['subjectOverride'], 'string:Update Software')
        self.assertEqual(mailer['recipientOverride'], 'string:test@mail.com')
        self.assertEqual(mailer['body_type'], 'html')

        self.assertEqual(mailer.created(), form.created())
        self.assertEqual(mailer.modified(), form.modified())

    def test_thanks_page(self):
        form = self.portal['post-software']
        self.failUnless('thank-you' in form)
        page = form['thank-you']

        self.assertEqual(page.Title(), 'The form was send to editor.')
        self.assertEqual(page.getThanksPrologue(), 
            '<p>Thank you for new content. Our editor will review your request.<br /></p>')

        self.assertEqual(page.created(), form.created())
        self.assertEqual(page.modified(), form.modified())

    def test_fields(self):
        form = self.portal['post-software']
        fields = ['fullname', 'email', 'softwaretitle', 'softwaredescription',
            'softwaresummary', 'version', 'devstage', 'license', 'supportcms',
            'developed', 'downloadurl', 'softwareurl', 'demourl', 'cms',
            'softwaredate', 'platforms']
        for i in fields:
            self.failUnless(i in form)

    #def test_able_to_add_document(self):
        #new_id = self.folder.invokeFactory('Document', 'my-page')
        #self.assertEquals('my-page', new_id)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestImport))
    return suite
