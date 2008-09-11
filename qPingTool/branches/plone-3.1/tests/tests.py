import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from base import FunctionalTestCase

def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='cmsinfo.productinfo',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        doctestunit.DocTestSuite(
            module='Products.qPingTool.PingTool',
            setUp=testing.setUp, tearDown=testing.tearDown),

        doctestunit.DocTestSuite(
            module='Products.qPingTool.adapter',
            setUp=testing.setUp, tearDown=testing.tearDown),

        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='cmsinfo.productinfo',
        #    test_class=TestCase),

        ztc.FunctionalDocFileSuite(
            'browser.txt', package='Products.qPingTool.tests',
            test_class=FunctionalTestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
