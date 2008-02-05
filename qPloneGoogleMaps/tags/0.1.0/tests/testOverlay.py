
""" This module contains class that tests Overlay content type """

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from commonTestingStuff import *

class TestOverlay(PloneTestCase.FunctionalTestCase, PloneTestCase.PloneTestCase):
    """ Test Overlay content type"""

    def afterSetUp(self):
        """ AfterSetUp features """
        self.loginAsPortalOwner()
        self.folder.invokeFactory("Map", "test_map")
        self.test_map = self.folder.test_map
        self.test_map.update(location=FIELD_VALUE)
        self.test_map.invokeFactory("Overlay", id="test_overlay", title="Test Overlay", description="Test Overlay Description")
        self.test_overlay = self.test_map.test_overlay
        self.fields = ['title' ,'description' ,'markerssource' ,'markerscolor']
        self.membership = getToolByName(self.portal, 'portal_membership', None)
        self.membership.addMember('another_member', user_password , ['Member'], [])
        maps_login(self, user_name)
        self.auth = user_name + ':' + user_password

    def testTypeInformation(self):
        """ Test Overlay factory type information """
        type_info = getToolByName(self.portal, 'portal_types').getTypeInfo("Overlay")
        self.assertEqual(type_info.global_allow, False)
        self.assertEqual(type_info.content_meta_type, "Overlay")

        ## actions
        actions = [a.id for a in type_info._actions]
        self.assertEqual(actions, ['view', 'edit', 'metadata', 'references', 'external_edit', 'local_roles'])

    def testOverlayInvoking(self):
        """ Test Overlay creating """
        test_overlay = self.test_overlay
        self.assertEqual(test_overlay.getId(), "test_overlay")
        self.assertEqual(test_overlay.Title(), "Test Overlay")
        self.assertEqual(test_overlay.Description(), "Test Overlay Description")

    def testUpdateOverlayForMember(self):
        """ Test possibility to update Overlay type for member with owner permissions """
        maps_login(self, 'member')
        object_id = self.test_map.invokeFactory('Overlay', 'test')
        object = getattr(self.test_map, object_id)
        object.update(title='test title')
        self.failUnless(object.Title() == 'test title', "Member can't update Map with owner permissions.")

    def testAuthenticatedUserAddOverlayContentType(self):
        """ Test possibility of adding Overlay content type by authenticated user """
        for user in ['member', 'manager']:
            maps_login(self, user)
            folder = self.folder
            if user == 'manager':
                folder = self.portal
            try:
                testMap = folder.invokeFactory('Map', 'testMap')
                example_id = folder.testMap.invokeFactory('Overlay', 'test_%s' % user)
            except Unauthorized: self.fail("%s could not create Overlay type" % user)
            self.failUnless(example_id in folder.testMap.objectIds(), "%s failed to add Overlay type to portal" % user)

    def testAnonymAddOverlayContentType(self):
        """Check impossibility of adding Overlay content type by anonymous user """
        maps_login(self, 'anonym')
        self.assertRaises(Unauthorized, self.test_map.invokeFactory, 'Overlay', 'test_example')

    def testAllFieldsPresence(self):
        """ Test for all fields presence in Overlay """
        missing_fields = [f for f in self.fields if not self.test_overlay.Schema().has_key(f)]
        self.failIf(missing_fields, "Following object's fields are missed: %s" % str(missing_fields) )

    def testFieldsAccessibilityView(self):
        """ Test fields accessibility for viewing """
        result = {'anonym':[], 'another_member':[], 'member':[], 'manager':[]}
        for user in ['anonym', 'another_member', 'member', 'manager']:
            maps_login(self, user)
            for f in self.fields:
                field = self.test_overlay.getField(f)
                if not field.checkPermission('view', self.test_overlay):
                    result[user].append(f)
            self.failIf(result[user], "%s - can't view fields: %s" % (user, str(result[user])))

    def testFieldsAllowedEditing(self):
        """ Test fields accessibility for editing owner and manager """
        result = {'anonym':[], 'another_member':[], 'member':[], 'manager':[]}
        # Allowed editing
        for user in ['member', 'manager']:
            maps_login(self, user)
            for f in self.fields:
                field = self.test_overlay.getField(f)
                if not field.checkPermission('edit', self.test_overlay):
                    result[user].append(f)
            self.failIf(result[user], "%s - can't edit fields: %s" % (user, str(result[user])))

    def testFieldsDisallowedEditing(self):
        """ Test fields accessibility for editing for member (not owner) and anonymous """
        result = {'anonym':[], 'another_member':[], 'member':[], 'manager':[]}
        # Disallowed editing
        for user in ['anonym', 'another_member']:
            maps_login(self, user)
            for f in self.fields:
                field = self.test_overlay.getField(f)
                if field.checkPermission('edit', self.test_overlay):
                    result[user].append(f)
            self.failIf(result[user], "%s - can edit fields: %s" % (user, str(result[user])) )

    def testGetMarkers(self):
        """ Test getMarkers Overlays' method """
        maps_login(self, 'member')
        self.folder.invokeFactory('Folder', 'source_folder')
        self.folder.source_folder.invokeFactory('Document', 'test_page')
        IGEOLocated(self.folder.source_folder.test_page).setLocation(FIELD_VALUE[0], FIELD_VALUE[1])
        self.folder.source_folder.test_page.reindexObject()
        self.test_overlay.update(markerscolor=OVERLAY_COLOR)
        self.test_overlay.update(markerssource=self.folder.source_folder)
        self.failUnless(self.test_overlay.getSource() == self.folder.source_folder,
                        "getMarkers method return incorrect result")
        self.failUnless(self.test_overlay.getMarkersColor() == OVERLAY_COLOR,
                        "getMarkers method return incorrect result")
        self.failUnless('test_page' == self.test_overlay.getMarkers()[0].getId,
                        "getMarkers method return incorrect result")

    def testGeneratedJavaScript(self):
        """ Test generated javascript for overlay_view template """
        data = {'longlat'          : self.test_overlay.getMarkers(),
                'color'            : self.test_overlay.getMarkersColor(),
                'loc'              : self.test_map.geoLocation(),
                'controls'         : self.test_map.getMapControl(),
                'typeControls'     : self.test_map.getTypeControl(),
                'overviewControls' : self.test_map.getOverviewControl(),
                'maptype'          : self.test_map.getMapType(),
                'node'             : 'mapView',
                'events'           : True
               }
        path = '%s/maps_markers' % self.test_overlay.absolute_url_path()
        response = self.publish(path, self.auth, extra=data, request_method="POST")
        self.failUnless(response.body == OVERLAY_VIEW_JAVASCRIPT,
                        "Incorrect javascript tag returned by maps_markers script")

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestOverlay))
    return suite

if __name__ == '__main__':
    framework()
