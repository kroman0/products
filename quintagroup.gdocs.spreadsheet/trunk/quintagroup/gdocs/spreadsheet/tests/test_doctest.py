import unittest
import doctest

import zope.component
from Testing import ZopeTestCase as ztc

from quintagroup.gauth.interfaces import IGAuthUtility
from quintagroup.gdocs.spreadsheet.tests import base


def setUp(test):

    """substitution using the adapter services gdata"""
    import quintagroup.gdocs.spreadsheet.tests.adapters


def test_suite():
    return unittest.TestSuite([

        # Demonstrate the main content types
        ztc.ZopeDocFileSuite(
            'README.txt', package='quintagroup.gdocs.spreadsheet',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            setUp=setUp,
            ),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
