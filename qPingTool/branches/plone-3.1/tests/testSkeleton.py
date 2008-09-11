#
# qPingTool TestCase
#

from Testing import ZopeTestCase

ZopeTestCase.installProduct('qPingTool')

class TestSomething(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        pass

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSomething))
    return suite
