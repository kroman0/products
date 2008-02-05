
""" This module contains class that tests Map content type """

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestMap(PloneTestCase.FunctionalTestCase, PloneTestCase.PloneTestCase):
    """ Test Map content type"""

    def afterSetUp(self):
        """ AfterSetUp features """
        self.loginAsPortalOwner()
        self.folder.invokeFactory("Map", id="test_map", title="Test Map", description="Test Map Description")
        self.test_map = self.folder.test_map
        self.fields = ['title' ,'description' ,'location' ,'auto', 'height', 'zoom', \
                       'mapControl', 'mapType', 'typeControl', 'overviewControl']
        self.membership = getToolByName(self.portal, 'portal_membership', None)
        self.membership.addMember('another_member', user_password , ['Member'], [])
        maps_login(self, user_name)
        self.auth = user_name + ':' + user_password
        self.test_map.setLocation(FIELD_VALUE)

    def testTypeInformation(self):
        """ Test Map factory type information """
        type_info = getToolByName(self.portal, 'portal_types').getTypeInfo("Map")
        self.assertEqual(type_info.global_allow, True)
        self.assertEqual(type_info.filter_content_types, True)
        self.assertEqual(type_info.allowed_content_types, ("Marker", "Overlay"))
        self.assertEqual(type_info.content_meta_type, "Map")

        ## actions
        actions = [a.id for a in type_info._actions]
        self.assertEqual(actions, ['view', 'edit', 'metadata', 'references', 'folderlisting', 'local_roles'])

    def testMapInvoking(self):
        """ Test Map creating """
        test_map = self.test_map
        self.assertEqual(test_map.getId(), "test_map")
        self.assertEqual(test_map.Title(), "Test Map")
        self.assertEqual(test_map.Description(), "Test Map Description")

    def testUpdateMapForMember(self):
        """ Test possibility to update Map type for member with owner permissions """
        maps_login(self, 'member')
        object_id = self.folder.invokeFactory('Map', 'test')
        object = getattr(self.folder, object_id)
        object.update(title='test title')
        self.failUnless(object.Title() == 'test title', "Member can't update Map with owner permissions.")

    def testAuthenticatedUserAddMapContentType(self):
        """ Test possibility of adding Map content type by authenticated user """
        for user in ['member', 'manager']:
            maps_login(self, user)
            folder = self.folder
            if user == 'manager':
                folder = self.portal
            try: example_id = folder.invokeFactory('Map', 'test_%s' % user)
            except Unauthorized: self.fail("%s could not create Map type" % user)
            self.failUnless(example_id in folder.objectIds(), "%s failed to add Map type to portal" % user)

    def testAnonymAddMapContentType(self):
        """Check impossibility of adding Map content type by anonymous user """
        maps_login(self, 'anonym')
        self.assertRaises(Unauthorized, self.folder.invokeFactory, 'Map', 'test_example')

    def testAllFieldsPresence(self):
        """ Test for all fields presence in Map """
        missing_fields = [f for f in self.fields if not self.test_map.Schema().has_key(f)]
        self.failIf(missing_fields, "Following object's fields are missed: %s" % str(missing_fields) )

    def testFieldsAccessibilityView(self):
        """ Test fields accessibility for viewing """
        result = {'anonym':[], 'another_member':[], 'member':[], 'manager':[]}
        for user in ['anonym', 'another_member', 'member', 'manager']:
            maps_login(self, user)
            for f in self.fields:
                field = self.test_map.getField(f)
                if not field.checkPermission('view', self.test_map):
                    result[user].append(f)
            self.failIf(result[user], "%s - can't view fields: %s" % (user, str(result[user])))

    def testFieldsAllowedEditing(self):
        """ Test fields accessibility for editing owner and manager """
        result = {'anonym':[], 'another_member':[], 'member':[], 'manager':[]}
        # Allowed editing
        for user in ['member', 'manager']:
            maps_login(self, user)
            for f in self.fields:
                field = self.test_map.getField(f)
                if not field.checkPermission('edit', self.test_map):
                    result[user].append(f)
            self.failIf(result[user], "%s - can't edit fields: %s" % (user, str(result[user])))

    def testFieldsDisallowedEditing(self):
        """ Test fields accessibility for editing for member (not owner) and anonymous """
        result = {'anonym':[], 'another_member':[], 'member':[], 'manager':[]}
        # Disallowed editing
        for user in ['anonym', 'another_member']:
            maps_login(self, user)
            for f in self.fields:
                field = self.test_map.getField(f)
                if field.checkPermission('edit', self.test_map):
                    result[user].append(f)
            self.failIf(result[user], "%s - can edit fields: %s" % (user, str(result[user])) )

    def testGeoLocationMethod(self):
        """ Test geoLocation Maps' method """
        self.assertEqual(self.test_map.geoLocation(), FIELD_VALUE, "geoLocation method return bad value")

    def testGetOverlayMarkersMethod(self):
        """ Test getOverlayMarkers Maps' method """
        maps_login(self, 'member')
        self.folder.invokeFactory('Folder', 'source_folder')
        self.folder.source_folder.invokeFactory('Document', 'test_page')
        IPoint(self.folder.source_folder.test_page).coordinates = (FIELD_VALUE[0], FIELD_VALUE[1], 0)
        self.folder.source_folder.test_page.reindexObject()
        self.test_map.invokeFactory('Overlay', 'test_overlay')
        self.test_map.test_overlay.update(markerscolor='green')
        self.test_map.test_overlay.update(markerssource=self.folder.source_folder)
        self.failUnless(('test_overlay', 'green') in self.test_map.getOverlayMarkers().keys(),
                         "getOverlayMarkers method return incorrect result")
        self.failUnless('test_page' == self.test_map.getOverlayMarkers().values()[0][0].getId,
                        "getOverlayMarkers method return incorrect result")

    def testGeneratedJavaScript(self):
        """ Test generated javascript for map_view template """
        test_map = self.test_map
        data = {'longlat'          : test_map.getOverlayMarkers(),
                'node'             : 'mapView',
                'controls'         : test_map.getMapControl(),
                'loc'              : test_map.geoLocation(),
                'typeControls'     : test_map.getTypeControl(),
                'overviewControls' : test_map.getOverviewControl(),
                'events'           : True,
                'maptype'          : test_map.getMapType(),
                'color'            : False,
                'zoom'             : test_map.getZoom(),
                'mapevents'        : True,
                'auto'             : test_map.getAuto()
               }
        path = '%s/maps_markers' % self.test_map.absolute_url_path()
        response = self.publish(path, self.auth, extra=data, request_method="POST")
        self.failUnless(response.body == MAP_VIEW_JAVASCRIPT,
                        "Incorrect javascript tag returned by maps_markers script")

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMap))
    return suite

if __name__ == '__main__':
    framework()
