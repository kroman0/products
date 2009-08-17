import unittest

from zope.testing import doctest, cleanup

from Products.Five import zcml

from collective.transmogrifier.tests import tearDown
from quintagroup.transmogrifier.tests import sectionsSetUp

import quintagroup.transmogrifier.simpleblog2quills.tests

def sourceSetUp(test):
    sectionsSetUp(test)
    zcml.load_config('test_import.zcml', quintagroup.transmogrifier.simpleblog2quills.tests)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests((
        doctest.DocFileSuite(
            'source.txt',
            setUp=sourceSetUp, tearDown=tearDown),
    ))
    return suite
