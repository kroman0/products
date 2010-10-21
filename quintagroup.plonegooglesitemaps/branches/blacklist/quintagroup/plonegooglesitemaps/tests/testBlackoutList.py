#
# Tests related to general Sitemap type.
#
from base import *
from zope.component import queryUtility

from quintagroup.plonegooglesitemaps.config import BLACKOUT_PREFIX
from quintagroup.plonegooglesitemaps.interfaces import IBlackoutFilterUtility


class TestBOFilterUtilities(TestCase):

    def testDefaultIdUtility(self):
        uname = BLACKOUT_PREFIX + "id"
        self.assertTrue(queryUtility(IBlackoutFilterUtility, name=uname) is not None,
            "Not registered default '%s' IBlackoutFilterUtility" % uname)

    def testDefaultPathUtility(self):
        uname = BLACKOUT_PREFIX + "path"
        self.assertTrue(queryUtility(IBlackoutFilterUtility, name=uname) is not None,
            "Not registered default '%s' IBlackoutFilterUtility" % uname)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBOFilterUtilities))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
#    framework()
