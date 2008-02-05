
""" This module contains class that tests product's utility module """


import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestUtility(PloneTestCase.PloneTestCase):
    """ Class for testing product utility module """

    def testProcessDesc(self):
        """ Test utility function processDesc: replace in a given string '\r\n' with ' ' and '\"' with '\'' """
        self.failUnless(processDesc(UNPROCESSED_STRING)==PROCESSED_STRING, 'Utility function processDesc fail')

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUtility))
    return suite

if __name__ == '__main__':
    framework()
