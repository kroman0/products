""" This module contains class that tests MapField and MapWidget """

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestMapField(PloneTestCase.PloneTestCase):
    """ Class for testing MapField and MapWidget """

    def afterSetUp(self):
        """ AfterSetUp features """
        self.loginAsPortalOwner()
        pt=self.portal.portal_types
        pt.constructContent('MapFieldTest', self.folder, 'mapfield')

    def testMapField(self):
        """ Test MapField """
        f = self.folder.mapfield
        f.update(location=FIELD_VALUE)
        r = f.getLocation()
        self.assertEqual(FIELD_VALUE[0], r[0])
        self.assertEqual(FIELD_VALUE[1], r[1])
        self.assertEqual(FIELD_VALUE, r)

    def testMapFieldAccessor(self):
        """ Test the map field accessor """
        f = self.folder.mapfield
        f.update(location=FIELD_VALUE)
        p = f.Schema()['location']
        self.assertEqual(p.getAccessor(f)(), FIELD_VALUE)

    def testMapWidget(self):
        """ Test MapWidget """
        instance = self.folder.mapfield
        field = instance.Schema()['location']
        #print field.widget.getName()
        form={'location_latitude'  : FIELD_VALUE[0],
              'location_longitude' : FIELD_VALUE[1],}
        result = field.widget.process_form(instance, field, form, empty_marker=[])
        self.assertEqual(result[0], FIELD_VALUE)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMapField))
    return suite

if __name__ == '__main__':
    framework()
