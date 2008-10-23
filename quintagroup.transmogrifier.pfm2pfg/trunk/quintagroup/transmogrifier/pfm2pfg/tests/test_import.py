import unittest
import os.path
import email

from zope.interface import classProvides, implements
import transaction

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

        fname = os.path.join(os.path.dirname(__file__), 'complex_form.xml')
        xml = file(fname).read()
        item = dict(
            _type='PloneFormMailer',
            _path='complex-form',
            _files=dict(
                marshall=dict(
                    name='.marshall.xml',
                    data=xml
                )
            )
        )
        yield item

        fname = os.path.join(os.path.dirname(__file__), 'fieldset_form.xml')
        xml = file(fname).read()
        item = dict(
            _type='PloneFormMailer',
            _path='fieldset-form',
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
        if 'complex-form' not in self.portal:
            # run transmogrifier pipeline
            transmogrifier = ITransmogrifier(self.portal)
            transmogrifier('test_import')

    def beforeTearDown(self):
        transaction.commit()

    def test_form_folder(self):
        self.failUnless('complex-form' in self.portal)
        form = self.portal['complex-form']

        self.assertEqual(form['title'], 'Test form')
        self.assertEqual(form.getFormPrologue(), '<p>form prologue</p>')
        self.assertEqual(form.getFormEpilogue(), '<p>form epilogue</p>')
        self.assertEqual(form['thanksPageOverride'], 'redirect_to:string:test')
        self.assertEqual(form['afterValidationOverride'], 'string:script')

    def test_mailer(self):
        form = self.portal['complex-form']
        self.failUnless('mailer' in form)
        mailer = form['mailer']

        self.assertEqual(mailer['subjectOverride'], 'string:Test form submit')
        self.assertEqual(mailer['recipient_name'], 'Test')
        self.assertEqual(mailer['recipientOverride'], 'string:recipient@mail.org')
        self.assertEqual(mailer['additional_headers'], ('Header1: value1', 'Header2: value2'))
        self.assertEqual(mailer['body_type'], 'html')
        self.assertEqual(mailer.getBody_pre(), 'Next are input fields')
        self.assertEqual(mailer.getBody_post(), 'You have filled all necessary fields')
        self.assertEqual(mailer.getBody_footer(), 'It\'s built on Plone')
        self.assertEqual(mailer['cc_recipients'], ('cc1@mail.org', 'cc2@mail.org'))
        self.assertEqual(mailer['bcc_recipients'], ('bcc1@mail.org', 'bcc2@mail.org'))

        self.assertEqual(mailer.created(), form.created())
        self.assertEqual(mailer.modified(), form.modified())

    def test_thanks_page(self):
        form = self.portal['complex-form']
        self.failUnless('thank-you' in form)
        page = form['thank-you']

        self.assertEqual(page.Title(), 'The form was sent.')
        self.assertEqual(page.getThanksPrologue(), 
            '<p>Thank you for submiting it.<br /></p>')

        self.assertEqual(page.created(), form.created())
        self.assertEqual(page.modified(), form.modified())

    def test_string_field(self):
        form = self.portal['complex-form']
        self.failIf('field1' not in form)
        field = form['field1']

        self.assertEqual(field.getPortalTypeName(), 'FormStringField')
        self.assertEqual(field['title'], 'String field')
        self.assertEqual(field.Description(), 'field description')
        self.assertEqual(field['required'], True)
        self.assertEqual(field['hidden'], False)
        self.assertEqual(field['fgDefault'], '')
        self.assertEqual(field['fgmaxlength'], 255)
        self.assertEqual(field['fgsize'], 20)

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_email_field(self):
        form = self.portal['complex-form']
        self.failIf('field2' not in form)
        field = form['field2']

        self.assertEqual(field.getPortalTypeName(), 'FormStringField')
        self.assertEqual(field['title'], 'Email field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['required'], True)
        self.assertEqual(field['hidden'], False)
        self.assertEqual(field['fgDefault'], 'test@mail.com')
        self.assertEqual(field['fgmaxlength'], 255)
        self.assertEqual(field['fgsize'], 20)
        self.assertEqual(field['fgStringValidator'], 'isEmail')

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_link_field(self):
        form = self.portal['complex-form']
        self.failIf('field3' not in form)
        field = form['field3']

        self.assertEqual(field.getPortalTypeName(), 'FormStringField')
        self.assertEqual(field['title'], 'Link field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['required'], False)
        self.assertEqual(field['hidden'], False)
        self.assertEqual(field['fgDefault'], '')
        self.assertEqual(field['fgmaxlength'], 15)
        self.assertEqual(field['fgsize'], 20)
        self.assertEqual(field['fgStringValidator'], 'isURL')

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_pattern_field(self):
        form = self.portal['complex-form']
        self.failIf('field4' not in form)
        field = form['field4']

        self.assertEqual(field.getPortalTypeName(), 'FormStringField')
        self.assertEqual(field['title'], 'Pattern field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['required'], True)
        self.assertEqual(field['hidden'], True)
        self.assertEqual(field['fgDefault'], '')
        self.assertEqual(field['fgmaxlength'], 255)
        self.assertEqual(field['fgsize'], 20)

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_textarea_field(self):
        form = self.portal['complex-form']
        self.failIf('field5' not in form)
        field = form['field5']

        self.assertEqual(field.getPortalTypeName(), 'FormTextField')
        self.assertEqual(field['title'], 'Text area field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['required'], True)
        self.assertEqual(field['hidden'], False)
        self.assertEqual(field.getFgDefault(), '')
        self.assertEqual(field['fgmaxlength'], 1000)
        self.assertEqual(field['fgRows'], 5)

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_rawtextarea_field(self):
        form = self.portal['complex-form']
        self.failIf('field6' not in form)
        field = form['field6']

        self.assertEqual(field.getPortalTypeName(), 'FormTextField')
        self.assertEqual(field['title'], 'Raw text area field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['required'], True)
        self.assertEqual(field['hidden'], False)
        self.assertEqual(field.getFgDefault(), '')
        self.assertEqual(field['fgmaxlength'], '0')
        self.assertEqual(field['fgRows'], 5)

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_password_field(self):
        form = self.portal['complex-form']
        self.failIf('field7' not in form)
        field = form['field7']

        self.assertEqual(field.getPortalTypeName(), 'FormPasswordField')
        self.assertEqual(field['title'], 'Password field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['required'], True)
        self.assertEqual(field['fgDefault'], '')
        self.assertEqual(field['fgmaxlength'], 255)
        self.assertEqual(field['fgsize'], 20)

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_label_field(self):
        form = self.portal['complex-form']
        self.failIf('field8' not in form)
        field = form['field8']

        self.assertEqual(field.getPortalTypeName(), 'FormRichLabelField')
        self.assertEqual(field['title'], 'Label field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['fgDefault'], 'label text')

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_integer_field(self):
        form = self.portal['complex-form']
        self.failIf('field9' not in form)
        field = form['field9']

        self.assertEqual(field.getPortalTypeName(), 'FormIntegerField')
        self.assertEqual(field['title'], 'Integer field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['required'], True)
        self.assertEqual(field['fgDefault'], '55')
        self.assertEqual(field['fgmaxlength'], 40)
        self.assertEqual(field['fgsize'], 20)
        self.assertEqual(field['minval'], 10)
        self.assertEqual(field['maxval'], 1000)

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_float_field(self):
        form = self.portal['complex-form']
        self.failIf('field10' not in form)
        field = form['field10']

        self.assertEqual(field.getPortalTypeName(), 'FormFixedPointField')
        self.assertEqual(field['title'], 'Float field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['required'], True)
        self.assertEqual(field['fgDefault'], '')
        self.assertEqual(field['fgmaxlength'], 10)
        self.assertEqual(field['fgsize'], 20)

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_datetime_field(self):
        form = self.portal['complex-form']
        self.failIf('field11' not in form)
        field = form['field11']

        self.assertEqual(field.getPortalTypeName(), 'FormDateField')
        self.assertEqual(field['title'], 'Date time field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['required'], True)
        self.assertEqual(field['fgDefault'], '2008/10/10 10:10:00 GMT+3')
        self.assertEqual(field['fgStartingYear'], 2006)
        self.assertEqual(field['fgEndingYear'], 2010)

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_file_field(self):
        form = self.portal['complex-form']
        self.failIf('field12' not in form)
        field = form['field12']

        self.assertEqual(field.getPortalTypeName(), 'FormFileField')
        self.assertEqual(field['title'], 'File field')
        self.assertEqual(field.Description(), '')

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_lines_field(self):
        form = self.portal['complex-form']
        self.failIf('field13' not in form)
        field = form['field13']

        self.assertEqual(field.getPortalTypeName(), 'FormLinesField')
        self.assertEqual(field['title'], 'Lines field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['required'], True)
        self.assertEqual(field['fgDefault'], ('first', 'second', 'third'))
        self.assertEqual(field['fgRows'], 5)

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_checkbox_field(self):
        form = self.portal['complex-form']
        self.failIf('field14' not in form)
        field = form['field14']

        self.assertEqual(field.getPortalTypeName(), 'FormBooleanField')
        self.assertEqual(field['title'], 'Checkbox field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['fgDefault'], True)

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_list_field(self):
        form = self.portal['complex-form']
        self.failIf('field15' not in form)
        field = form['field15']

        self.assertEqual(field.getPortalTypeName(), 'FormSelectionField')
        self.assertEqual(field['title'], 'List field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['fgDefault'], 'first')
        self.assertEqual(field['fgVocabulary'], ('first|First', 'second|Second', 'third|Third'))
        self.assertEqual(field['fgFormat'], 'select')

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_radio_field(self):
        form = self.portal['complex-form']
        self.failIf('field16' not in form)
        field = form['field16']

        self.assertEqual(field.getPortalTypeName(), 'FormSelectionField')
        self.assertEqual(field['title'], 'Radio field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['fgDefault'], 'first')
        self.assertEqual(field['fgVocabulary'], ('first|First', 'second|Second', 'third|Third'))
        self.assertEqual(field['fgFormat'], 'radio')

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_multilist_field(self):
        form = self.portal['complex-form']
        self.failIf('field17' not in form)
        field = form['field17']

        self.assertEqual(field.getPortalTypeName(), 'FormMultiSelectionField')
        self.assertEqual(field['title'], 'Multi list field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['required'], True)
        self.assertEqual(field['fgDefault'], ('first', 'third'))
        self.assertEqual(field['fgVocabulary'], ('first|First', 'second|Second', 'third|Third'))
        self.assertEqual(field['fgFormat'], 'select')
        self.assertEqual(field['fgRows'], 5)

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_multicheckbox_field(self):
        form = self.portal['complex-form']
        self.failIf('field18' not in form)
        field = form['field18']

        self.assertEqual(field.getPortalTypeName(), 'FormMultiSelectionField')
        self.assertEqual(field['title'], 'Multi checkbox field')
        self.assertEqual(field.Description(), '')
        self.assertEqual(field['required'], True)
        self.assertEqual(field['fgDefault'], ('first', 'third'))
        self.assertEqual(field['fgVocabulary'], ('first|First', 'second|Second', 'third|Third'))
        self.assertEqual(field['fgFormat'], 'checkbox')

        self.assertEqual(field.created(), form.created())
        self.assertEqual(field.modified(), form.modified())

    def test_fieldset(self):
        self.failIf('fieldset-form' not in self.portal)
        form = self.portal['fieldset-form']
        self.assertEqual(form.objectIds(), ['mailer', 'thank-you', 'checkbox', 'datetime', 'Other'])

        fieldset = form['Other']
        self.assertEqual(fieldset['title'], 'Other')
        self.assertEqual(fieldset.objectIds(), ['email', 'float', 'string'])

class FakeRequest(dict):

    def __init__(self, **kwargs):
        self.form = kwargs

class TestSubmit(ptc.PloneTestCase):
    """ test ya_gpg.py """

    def dummy_send(self, mfrom, mto, messageText):
        self.mfrom = mfrom
        self.mto = mto
        self.messageText = messageText

    def afterSetUp(self):
        transmogrifier = ITransmogrifier(self.portal)
        transmogrifier('test_import')
        self.form = getattr(self.folder, 'complex-form')
        for i in self.form.contentValues():
            field = i.getField('required')
            if field is not None:
                field.getMutator(i)(False)
        self.mailhost = self.folder.MailHost
        self.mailhost._send = self.dummy_send

    def test_submitting(self):
        """ Test submitting of form """
        request = FakeRequest(field2='field2@mail.org')
        errors = self.form.fgvalidate(REQUEST=request)
        msg = email.message_from_string(self.messageText)
        self.assertEqual(msg.get('To'), 'Test <recipient@mail.org>')
        self.assertEqual(msg.get('Subject'), '=?utf-8?q?Test_form_submit?=')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestImport))
    suite.addTest(unittest.makeSuite(TestSubmit))
    return suite
