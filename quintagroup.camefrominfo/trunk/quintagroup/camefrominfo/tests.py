import unittest
import os
import sys
import re

from unittest import makeSuite, TestCase
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import quintagroup.camefrominfo
from zope.testbrowser.browser import Browser

class CameFromInfoTest(TestCase):

    def setUp(self):
        pass

    def test_camefrominfo(self):
        pass

def test_suite():
    return makeSuite(CameFromInfoTest)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
