import re
import string
import unittest
import transaction

from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase.layer import onsetup

from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase import setup as ptc_setup

from Products.PloneTestCase.PloneTestCase import portal_owner
from Products.PloneTestCase.PloneTestCase import default_password

PACKAGES = [
    'quintagroup.captcha.core',
    'quintagroup.pfg.captcha',
]
PROFILES = [p+':default' for p in PACKAGES]
REQUIREMENTS = ['PloneFormGen',] + PACKAGES

ptc.setupPloneSite()

class NotInstalled(PloneSite):
    """ Only package register, without installation into portal
    """
    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        import quintagroup.pfg.captcha
        zcml.load_config('configure.zcml', quintagroup.pfg.captcha)
        fiveconfigure.debug_mode = False
        ztc.installProduct('PloneFormGen')
        ztc.installPackage('quintagroup.pfg.captcha')
        ztc.installPackage('quintagroup.captcha.core')


class Installed(NotInstalled):
    """ Install product into the portal
    """
    @classmethod
    def setUp(cls):
        app = ztc.app()
        portal = app[ptc_setup.portal_name]

        # Sets the local site/manager
        ptc_setup._placefulSetUp(portal)
        # Install PROJECT
        qi = getattr(portal, 'portal_quickinstaller', None)
        for p in REQUIREMENTS:
            qi.installProduct(p)
        transaction.commit()

    @classmethod
    def tearDown(cls):
        ptc_setup._placefulTearDown()
        

class TestCase(ptc.PloneTestCase):
    layer = Installed

class TestCaseNotInstalled(ptc.PloneTestCase):
    layer = NotInstalled
