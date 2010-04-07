import unittest

from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase import PloneTestCase as ptc

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


def test_suite():
    suite = unittest.TestSuite()
    return suite
