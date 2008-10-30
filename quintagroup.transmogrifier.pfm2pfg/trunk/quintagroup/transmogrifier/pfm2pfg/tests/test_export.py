import time
import unittest
from xml.dom import minidom

from Testing import ZopeTestCase
from Products.CMFPlone.tests.PloneTestCase import PloneTestCase
from Products.Marshall.registry import getComponent

from quintagroup.transmogrifier.pfm2pfg.exporting import PloneFormMailerExporter

ZopeTestCase.installProduct('Formulator')
ZopeTestCase.installProduct('MimetypesRegistry')
ZopeTestCase.installProduct('PortalTransforms')
ZopeTestCase.installProduct('Archetypes')
ZopeTestCase.installProduct('PloneFormMailer')
ZopeTestCase.installProduct('TALESField')

def setupPloneFormMailerTestCase(app, quiet=0):
    get_transaction().begin()
    _start = time.time()
    if not quiet:
        ZopeTestCase._print('Adding PloneFormMailer ... ')
    app.portal.portal_quickinstaller.installProduct('PloneFormMailer')
    get_transaction().commit()
    if not quiet:
        ZopeTestCase._print('done (%.3fs)\n' % (time.time()-_start,))

app = ZopeTestCase.app()
setupPloneFormMailerTestCase(app, quiet=True)
ZopeTestCase.close(app)

class TestExport(PloneTestCase):
    """Test case for proping up a test portal."""
    def afterSetUp(self):
        self.loginPortalOwner()
        self.portal.invokeFactory('PloneFormMailer', id='form')
        form = self.portal.form
        ['recipient_name', 'bcc_recipients', 'cc_recipients']
        form.setRecipientName("string:Recipient")
        form.setCCRecipients([
            'string:cc1@mail.org',
            'string:cc2@mail.org'
        ])
        form.setBCCRecipients([
            'string:bcc1@mail.org',
            'string:bcc2@mail.org'
        ])
        form.setSubject('string:Email subject')

    def _testField(self, xml, name, values):
        """ Check whether marshalled in xml format field has some values.
        """
        doc = minidom.parseString(xml)
        elems = [i for i in doc.getElementsByTagName('field') if i.getAttribute('name') == name]
        if type(values) not in (list, tuple):
            values = [values]
        fields = []
        for i in elems:
            fields.append(i.firstChild.nodeValue.strip())
        return values == fields

    def test_data_corrector(self):
        _, _, xml = getComponent('atxml').marshall(self.portal.form)
        data = {'name': '', 'data': xml}
        #import pdb; pdb.set_trace()
        adapter = PloneFormMailerExporter(self.portal.form)
        adapter(data)
        xml = data['data']
        self.assertEqual(self._testField(xml, 'recipient_name', 'Recipient'), True)
        self.assertEqual(
            self._testField(xml,
                'cc_recipients',
                ['cc1@mail.org', 'cc2@mail.org']),
            True
        )
        self.assertEqual(
            self._testField(xml,
                'bcc_recipients',
                ['bcc1@mail.org', 'bcc2@mail.org']),
            True
        )
        self.assertEqual(self._testField(xml, 'subject', 'string:Email subject'), True)

    def test_bad_tales_field(self):
        self.portal.form.setRecipientName("bad tales expression")
        _, _, xml = getComponent('atxml').marshall(self.portal.form)
        data = {'name': '', 'data': xml}
        #import pdb; pdb.set_trace()
        adapter = PloneFormMailerExporter(self.portal.form)
        adapter(data)
        xml = data['data']
        #import pdb; pdb.set_trace()
        self.assertEqual(self._testField(xml, 'recipient_name', 'bad tales expression'), False)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestExport))
    return suite
