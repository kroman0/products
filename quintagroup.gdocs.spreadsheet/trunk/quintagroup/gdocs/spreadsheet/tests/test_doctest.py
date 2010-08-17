import unittest
import doctest

import zope.component
from Testing import ZopeTestCase as ztc

from quintagroup.gauth.interfaces import IGAuthUtility
import quintagroup.gdocs.spreadsheet.content.gspreadsheet as gspreadsheet
from quintagroup.gdocs.spreadsheet.tests import base


def setUp(test):

    """substitution using the adapter services gdata"""
    import quintagroup.gdocs.spreadsheet.tests.adapters


def tearDown(test):
    """This is the companion to setUp - it can be used to clean up the
    test environment after each test.
    """

def test_suite():
    return unittest.TestSuite([

        # Demonstrate the main content types
        ztc.ZopeDocFileSuite(
            'README.txt', package='quintagroup.gdocs.spreadsheet',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            setUp=setUp,
            tearDown=tearDown,
            ),
        ztc.ZopeDocFileSuite('tests/test_adapters.txt',
            package='quintagroup.gdocs.spreadsheet',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            setUp=setUp,
            tearDown=tearDown,
            ),
        ztc.ZopeDocFileSuite('tests/test_context.txt',
            package='quintagroup.gdocs.spreadsheet',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            setUp=setUp,
            tearDown=tearDown,
            ),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
