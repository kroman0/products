import unittest
import os
import sys
import re

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.PloneTestCase import portal_owner
from Products.PloneTestCase.PloneTestCase import default_password

from Products.CMFCore.utils import getToolByName

from quintagroup.captcha.core.config import *
from quintagroup.captcha.core.utils import getWord, decrypt, parseKey

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import quintagroup.captcha.core
    zcml.load_config('configure.zcml', quintagroup.captcha.core)
    fiveconfigure.debug_mode = False
    ztc.installPackage('quintagroup.captcha.core')

setup_product()
ptc.setupPloneSite()
