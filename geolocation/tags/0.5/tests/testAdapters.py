
""" This module contains class that tests products' adapters """

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestForInterfaces(PloneTestCase.PloneTestCase):
    """ Class for testing adapters' and browsers' for interfaces """

    def testAdapterInterface(self):
        """ Test adapters' for intefaces """
        verifyClass(IGEOLocated, GEOLocated)
        verifyClass(IGEOMap, GEOMap)

    def testBrowserInterface(self):
        """ Test browsers' for intefaces """
        verifyClass(IGEOLocatedView, GEOLocatedView)
        verifyClass(IGEOMapView, GEOMapView)

class TestGEOLocatedAdapter(PloneTestCase.PloneTestCase):
    """ Class for testing GEOLocated adapter """

    def afterSetUp(self):
        """ AfterSetUp features """
        self.folder.invokeFactory('Document', 'test_page')
        self.page = self.folder.test_page
        self.adapter = IGEOLocated(self.page)
        self.adapter.geolocation['latitude'] = LATITUDE
        self.adapter.geolocation['longitude'] = LONGITUDE

    def testImplementation(self):
        """ Test adapter implementation """
        IGEOLocated.implementedBy(GEOLocated)

    def testGetters(self):
        """ Test adapters' getters """
        self.failUnlessEqual(self.adapter.getLongitude(), LONGITUDE)
        self.failUnlessEqual(self.adapter.getLatitude(), LATITUDE)

    def testSetters(self):
        """ Test adapters' setters """
        adapter = IGEOLocated(self.page)
        adapter.setLatitude(LATITUDE)
        adapter.setLongitude(LONGITUDE)
        self.failUnlessEqual(self.adapter.geolocation['latitude'], LATITUDE)
        self.failUnlessEqual(self.adapter.geolocation['longitude'], LONGITUDE)

    def testSetLocationMethod(self):
        """ Test setLocation adapters' method """
        IGEOLocated(self.page).setLocation(LATITUDE, LONGITUDE)
        self.failUnlessEqual(self.adapter.geolocation['latitude'], LATITUDE)
        self.failUnlessEqual(self.adapter.geolocation['longitude'], LONGITUDE)

class TestGEOMapAdapter(PloneTestCase.PloneTestCase):
    """ Class for testing GEOMap adapter """

    def afterSetUp(self):
        """ AfterSetUp features """
        self.folder.invokeFactory('Document', 'test_page')
        self.page = self.folder.test_page
        self.adapter = IGEOMap(self.page)
        self.adapter.geomap['mapcenter'] = MAP_CENTER
        self.adapter.geomap['mapzoom']   = MAP_ZOOM
        self.adapter.geomap['maptype']   = MAP_TYPE

    def testImplementation(self):
        """ Test adapter implementation """
        IGEOMap.implementedBy(GEOMap)

    def testGetters(self):
        """ Test adapters' getters """
        self.failUnlessEqual(self.adapter.getMapCenter(), MAP_CENTER)
        self.failUnlessEqual(self.adapter.getMapZoom(), MAP_ZOOM)
        self.failUnlessEqual(self.adapter.getMapType(), MAP_TYPE)

    def testSetMapMethod(self):
        """ Test setMap adapters' method """
        IGEOMap(self.page).setMap(MAP_CENTER, MAP_ZOOM, MAP_TYPE)
        self.failUnlessEqual(self.adapter.geomap['mapcenter'], MAP_CENTER)
        self.failUnlessEqual(self.adapter.geomap['mapzoom'], MAP_ZOOM)
        self.failUnlessEqual(self.adapter.geomap['maptype'], MAP_TYPE)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestForInterfaces))
    suite.addTest(makeSuite(TestGEOLocatedAdapter))
    suite.addTest(makeSuite(TestGEOMapAdapter))
    return suite

if __name__ == '__main__':
    framework()
