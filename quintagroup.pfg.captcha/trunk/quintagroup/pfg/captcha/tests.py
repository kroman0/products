import re
import unittest

from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase import PloneTestCase as ptc

PRODUCTS = [
    'Products.PloneFormGen',
    'quintagroup.captcha.core',
    'quintagroup.pfg.captcha',
]
PROFILES = [p+':default' for p in PRODUCTS]

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import quintagroup.pfg.captcha
    zcml.load_config('configure.zcml', quintagroup.pfg.captcha)
    fiveconfigure.debug_mode = False
    ztc.installPackage('quintagroup.pfg.captcha')
    ztc.installPackage('quintagroup.captcha.core')

setup_product()
ptc.setupPloneSite(extension_profiles=PROFILES)


def test_suite():
    suite = unittest.TestSuite()
    return suite
