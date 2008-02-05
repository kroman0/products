
""" This module contains class that tests Marker content type """

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestMarker(PloneTestCase.FunctionalTestCase):
    """ Test Marker content type"""

    def afterSetUp(self):
        """ AfterSetUp features """
        self.loginAsPortalOwner()
        self.folder.invokeFactory("Map", "test_map")
        self.test_map = self.folder.test_map
        self.test_map.update(location=FIELD_VALUE)
        self.test_map.invokeFactory("Marker", id="test_marker", title="Test Marker", description="Test Marker Description")
        self.test_marker = self.test_map.test_marker
        self.test_marker.update(location=FIELD_VALUE)
        self.fields = ['title' ,'description' ,'location' ,'color']
        self.membership = getToolByName(self.portal, 'portal_membership', None)
        self.membership.addMember('another_member', user_password , ['Member'], [])
        maps_login(self, user_name)
        self.auth = user_name + ':' + user_password

    def testTypeInformation(self):
        """ Test Marker factory type information """
        type_info = getToolByName(self.portal, 'portal_types').getTypeInfo("Marker")
        self.assertEqual(type_info.global_allow, True)
        self.assertEqual(type_info.content_meta_type, "Marker")

        ## actions
        actions = [a.id for a in type_info._actions]
        self.assertEqual(actions, ['view', 'edit', 'metadata', 'references', 'history', 'external_edit', 'local_roles'])

    def testMarkerInvoking(self):
        """ Test Marker creating """
        test_marker = self.test_marker
        self.assertEqual(test_marker.getId(), "test_marker")
        self.assertEqual(test_marker.Title(), "Test Marker")
        self.assertEqual(test_marker.Description(), "Test Marker Description")

    def testUpdateMarkerForMember(self):
        """ Test possibility to update Marker type for member with owner permissions """
        maps_login(self, 'member')
        object_id = self.test_map.invokeFactory('Marker', 'test')
        object = getattr(self.test_map, object_id)
        object.update(title='test title')
        self.failUnless(object.Title() == 'test title', "Member can't update Map with owner permissions.")

    def testAuthenticatedUserAddMarkerContentType(self):
        """ Test possibility of adding Marker content type by authenticated user """
        for user in ['member', 'manager']:
            maps_login(self, user)
            folder = self.folder
            if user == 'manager':
                folder = self.portal
            try:
                example_id = folder.invokeFactory('Marker', 'test_%s' % user)
            except Unauthorized: self.fail("%s could not create Marker type" % user)
            self.failUnless(example_id in folder.objectIds(), "%s failed to add Marker type to portal" % user)

    def testAnonymAddMarkerContentType(self):
        """Check impossibility of adding Marker content type by anonymous user """
        maps_login(self, 'anonym')
        self.assertRaises(Unauthorized, self.folder.invokeFactory, 'Marker', 'test_example')

    def testAllFieldsPresence(self):
        """ Test for all fields presence in Marker """
        missing_fields = [f for f in self.fields if not self.test_marker.Schema().has_key(f)]
        self.failIf(missing_fields, "Following object's fields are missed: %s" % str(missing_fields) )

    def testFieldsAccessibilityView(self):
        """ Test fields accessibility for viewing """
        result = {'anonym':[], 'another_member':[], 'member':[], 'manager':[]}
        for user in ['anonym', 'another_member', 'member', 'manager']:
            maps_login(self, user)
            for f in self.fields:
                field = self.test_marker.getField(f)
                if not field.checkPermission('view', self.test_marker):
                    result[user].append(f)
            self.failIf(result[user], "%s - can't view fields: %s" % (user, str(result[user])))

    def testFieldsAllowedEditing(self):
        """ Test fields accessibility for editing owner and manager """
        result = {'anonym':[], 'another_member':[], 'member':[], 'manager':[]}
        # Allowed editing
        for user in ['member', 'manager']:
            maps_login(self, user)
            for f in self.fields:
                field = self.test_marker.getField(f)
                if not field.checkPermission('edit', self.test_marker):
                    result[user].append(f)
            self.failIf(result[user], "%s - can't edit fields: %s" % (user, str(result[user])))

    def testFieldsDisallowedEditing(self):
        """ Test fields accessibility for editing for member (not owner) and anonymous """
        result = {'anonym':[], 'another_member':[], 'member':[], 'manager':[]}
        # Disallowed editing
        for user in ['anonym', 'another_member']:
            maps_login(self, user)
            for f in self.fields:
                field = self.test_marker.getField(f)
                if field.checkPermission('edit', self.test_marker):
                    result[user].append(f)
            self.failIf(result[user], "%s - can edit fields: %s" % (user, str(result[user])) )

    def testGeoLocation(self):
        """ Test geoLocation Markers' method """
        maps_login(self, 'member')
        self.failUnless(self.test_marker.geoLocation() == FIELD_VALUE,
                        "geoLocation method return incorrect result")

    def testGeneratedJavaScript(self):
        """ Test generated javascript for marker_view template """
        data = {'longlat'          : self.portal.portal_catalog(path=self.test_marker.absolute_url_path()),
                'color'            : self.test_marker.getColor(),
                'loc'              : self.test_marker.geoLocation(),
                'controls'         : 'large',
                'typeControls'     : True,
                'overviewControls' : True,
                'node'             : 'mapView',
                'events'           : True,
                'zoom'             : 6,
                'auto'             : 'None'
               }
        path = '%s/maps_markers' % self.test_marker.absolute_url_path()
        response = self.publish(path, self.auth, extra=data, request_method="POST")
        self.failUnless(response.body == MARKER_VIEW_JAVASCRIPT,
                        "Incorrect javascript tag returned by maps_markers script")

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMarker))
    return suite

if __name__ == '__main__':
    framework()
