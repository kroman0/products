import unittest

from zope.interface import alsoProvides
from zope.schema.interfaces import IField
from zope.component import queryMultiAdapter
from zope.publisher.browser import TestRequest

from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import IValidator
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IErrorViewSnippet

from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase import PloneTestCase as ptc

from quintagroup.z3cform.captcha import Captcha
from quintagroup.z3cform.captcha import CaptchaWidget
from quintagroup.z3cform.captcha.widget import CaptchaWidgetFactory

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    # Register z3c namespace first
    import z3c.form
    zcml.load_config('meta.zcml', z3c.form)
    # Now register quintagroup.z3cform.captcha package
    import quintagroup.captcha.core
    import quintagroup.z3cform.captcha
    zcml.load_config('configure.zcml', quintagroup.z3cform.captcha)
    fiveconfigure.debug_mode = False
    ztc.installPackage('quintagroup.captcha.core')

setup_product()
ptc.setupPloneSite(extension_profiles=['quintagroup.captcha.core:default',])


class TestRegistrations(ptc.PloneTestCase):

    def afterSetUp(self):
        super(TestRegistrations, self).afterSetUp()
        self.request = self.app.REQUEST
        alsoProvides(self.request, IFormLayer)

    def testCaptchaFieldInterface(self):
        self.assertEqual(IField.implementedBy(Captcha), True)

    def testCaptchaWidgetInterface(self):
        self.assertEqual(IFieldWidget.implementedBy(CaptchaWidgetFactory), True)

    def testWidgetRegistration(self):
        cfield = Captcha()
        cwidget = queryMultiAdapter((cfield, self.request), IFieldWidget)
        self.assertNotEqual(cwidget, None)

    def testValidatorRegistration(self):
        cfield = Captcha()
        cvalidator = queryMultiAdapter((None, self.request, None, cfield, None),
                IValidator)
        self.assertNotEqual(cvalidator, None)

    def testErrorViewRegistration(self):
        cfield = Captcha()
        cwidget = queryMultiAdapter((cfield, self.request), IFieldWidget)
        error = ValueError()
        eview = queryMultiAdapter(
            (error, self.request, cwidget, cfield, None, None),
            IErrorViewSnippet)
        self.assertNotEqual(eview, None)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRegistrations))
    return suite
