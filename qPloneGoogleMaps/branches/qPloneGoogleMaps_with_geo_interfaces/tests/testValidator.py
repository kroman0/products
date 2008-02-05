
""" This module contains class that tests products' validator """


import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestValidator(PloneTestCase.PloneTestCase):
    """ Class for testing products' validator """

    def testNoneValue(self):
        """ Test validator with None value, have to return 1 """
        v = validator.MapFieldValidator(self)
        self.failUnlessEqual(v(None), 1)

    def testEmptyValues(self):
        """ Test validator with empty latitude and longitude values """
        v = validator.MapFieldValidator(self)
        self.failUnlessEqual(v(('', '')), " This field is required. ")

    def testNonTupleValue(self):
        """ Test validator with non tuple input value """
        v = validator.MapFieldValidator(self)
        self.failUnlessEqual(v('Bad format'), " Validation failed. Unexpected field value. ")

    def testNonDecimalValues(self):
        """ Test validator with none decimal values """
        v = validator.MapFieldValidator(self)
        self.failUnlessEqual(v(('bad decimal', 22.3)), " Validation failed. Coordinates must be an decimal numbers. ")

    def testUnBoundingLatitude(self):
        """ Test validator with latitude out of the bounds """
        v = validator.MapFieldValidator(self)
        self.failUnlessEqual(v((90.5, 45)), " Validation failed. Latitude not in bounds [-90, 90]. ")

    def testUnBoundingLongitude(self):
        """ Test validator with longitude out of the bounds """
        v = validator.MapFieldValidator(self)
        self.failUnlessEqual(v((45, -181.5)), " Validation failed. Longitude not in bounds [-180, 180]. ")

    def testGoodInput(self):
        """ Test validator good input value """
        v = validator.MapFieldValidator(self)
        self.failUnlessEqual(v((9.8, 10.3)), 1)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestValidator))
    return suite

if __name__ == '__main__':
    framework()