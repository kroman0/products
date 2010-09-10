import unittest
import doctest

from zope.interface import Interface

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Testing import ZopeTestCase as ztc

class FormlibCaptchaLayer(PloneSite):
    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        import quintagroup.captcha.core
        import quintagroup.formlib.captcha
        zcml.load_config('configure.zcml', quintagroup.formlib.captcha)
        zcml.load_config('tests.zcml', quintagroup.formlib.captcha.tests)
        fiveconfigure.debug_mode = False
        ztc.installPackage('quintagroup.captcha.core')

    @classmethod
    def tearDown(cls):
        pass
    
ptc.setupPloneSite(extension_profiles=['quintagroup.captcha.core:default',])


class FormlibCaptchaTestCase(ptc.FunctionalTestCase):
    layer = FormlibCaptchaLayer

def test_suite():
    return unittest.TestSuite([

        # Demonstrate the main content types
        ztc.ZopeDocFileSuite(
            'README.txt', package='quintagroup.formlib.captcha',
            test_class=FormlibCaptchaTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
            
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
