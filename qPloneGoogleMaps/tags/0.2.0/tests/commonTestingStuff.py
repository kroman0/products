from AccessControl import Unauthorized
from zope.app.tests import ztapi
from zope.app.annotation import IAttributeAnnotatable
from zope.interface import directlyProvides
from zope.interface.verify import verifyClass
from Testing.ZopeTestCase.PortalTestCase import user_name, user_password

from Products.CMFCore.utils import getToolByName

from Products.geolocation.interfaces.geolocation import IGEOLocated

from Products.qPloneGoogleMaps.adapters.markers import MarkersListing
from Products.qPloneGoogleMaps.browser.markersview import MarkersView
from Products.qPloneGoogleMaps.interfaces.markers import IMarkersListing, IMarkersView
from Products.qPloneGoogleMaps import validator
from Products.qPloneGoogleMaps.utility import processDesc
from Products.qPloneGoogleMaps.content import Map, Overlay, Marker

import MapFieldTest

from Products.PloneTestCase import PloneTestCase

PRODUCTS=('geolocation', 'qPloneGoogleMaps')

map(PloneTestCase.installProduct, PRODUCTS)
PloneTestCase.setupPloneSite(products=PRODUCTS)

PRODUCT = 'qPloneGoogleMaps'

def maps_login(self, role):
    """  Utility method for login under required role """
    from Testing.ZopeTestCase.PortalTestCase import user_name, user_password
    if role == 'manager':
        self.loginAsPortalOwner()
    elif role == 'member':
        self.login(user_name)
    elif role == 'another_member':
        self.login('another_member')
    elif role == 'anonym':
        self.logout()

# Installation testing stuff
NEW_PORTAL_TYPES = ['Map', 'Marker', 'Overlay']
MAP_API_KEYS = ("http://localhost.com:8888/map|ABQIAAAAPKXXAksH6LF9wD3-iB3Z9hR-_Derz1M-sZYUdeXG3J1uZOMrKxT98efydo7fhYu6kuaFv5ESjlw4mw", )
TOPIC_VIEW = 'topic_maps_view'
MAP_PORTLETS = ['here/portlet_maps/macros/portlet', 'here/portlet_overlays/macros/portlet',]
PROPERTY_SHEET = 'maps_properties'
PROPERTY_FIELD = 'map_api_keys'
GEO_INDEX = 'geoLocation'

# Utils testing stuff
UNPROCESSED_STRING = """This is "unprocessed" string
with carriage return and double
quotes."""
PROCESSED_STRING = "This is 'unprocessed' string with carriage return and double quotes."

# Validation testing stuff

# Field and widget testing stuff
FIELD_VALUE = (3.5, 20.4)

# Functional testing stuff
NEW_MAP_KEY = "http://nohost/plone|IAAAAPKXXAksH6LF9wD3-iB3Z9hR-_Derz1M-sZYUdeXG3J1uZOMrKxT98efydo7fhYu6kuaFv5ES"

# Map testing stuff
MAP_VIEW_JAVASCRIPT = """
<script type="text/javascript">
//<![CDATA[

function onLoadMap(){
  if (GBrowserIsCompatible()) {

    map1 = new GMap2(document.getElementById('mapView'));
    map1.addControl(new GLargeMapControl());
map1.addControl(new GMapTypeControl());
map1.addControl(new GOverviewMapControl());

    map1.setCenter(new GLatLng(3.500000, 20.400000), 3, G_HYBRID_MAP);
    var opt = map1.getInfoWindow(), overLays = {};
    opt.maxWidth = 400;

    var icon = new GIcon();
    icon.shadow = "http://nohost/plone/images/map_shadow.png";
    icon.iconSize = new GSize(20, 34);
    icon.shadowSize = new GSize(37, 34);
    icon.iconAnchor = new GPoint(9, 34);
    icon.infoWindowAnchor = new GPoint(9, 2);

    function addMarker(lat, lng, title, url, content, col){
      icon.image = "http://nohost/plone/images/"+col+"/map_marker.png";
      var point = new GLatLng(lat, lng);
      var marker = new GMarker(point, icon)
      map1.addOverlay(marker);
      
      var f = function(){marker.openInfoWindowHtml(
"<div><h2><a href='"+url+"'>"+title+"</a></h2><p>"+content+"</p></div>"
, opt);};
      GEvent.addListener(marker, 'click', f);

    };

    
    
    

    if (typeof(getData) == 'function') {
        var over_obj = getData();
        if (over_obj) {
            for (var i=0; i < over_obj['boxes'].length; i++) registerEventListener(over_obj['boxes'][i], 'click',
                function (){
                    map1.clearOverlays();
                    var bs = getData();
                    for (id in bs) {
                        if (bs[id] == true) {
                            for (var j=0; j < overLays[id].length; j++) {
                                var opts = overLays[id][j];
                                addMarker(opts[0], opts[1], opts[2], opts[3], opts[4], opts[5]);
                            };
                        }
                    };
                });
        }
    };

  }
  else window.alert("Google maps aren't compatible with current browser or your map api key doesn't match your portal root.");
};

registerEventListener(window, 'load', onLoadMap);
registerEventListener(window, 'unload', GUnload);

//]]>
</script>
"""

# Overlay testing stuff
OVERLAY_COLOR = 'blue'

OVERLAY_VIEW_JAVASCRIPT = """
<script type="text/javascript">
//<![CDATA[

function onLoadMap(){
  if (GBrowserIsCompatible()) {

    map1 = new GMap2(document.getElementById('mapView'));
    map1.addControl(new GLargeMapControl());
map1.addControl(new GMapTypeControl());
map1.addControl(new GOverviewMapControl());

    map1.setCenter(new GLatLng(3.500000, 20.400000), 6, G_HYBRID_MAP);
    var opt = map1.getInfoWindow(), overLays = {};
    opt.maxWidth = 400;

    var icon = new GIcon();
    icon.shadow = "http://nohost/plone/images/map_shadow.png";
    icon.iconSize = new GSize(20, 34);
    icon.shadowSize = new GSize(37, 34);
    icon.iconAnchor = new GPoint(9, 34);
    icon.infoWindowAnchor = new GPoint(9, 2);

    function addMarker(lat, lng, title, url, content, col){
      icon.image = "http://nohost/plone/images/"+col+"/map_marker.png";
      var point = new GLatLng(lat, lng);
      var marker = new GMarker(point, icon)
      map1.addOverlay(marker);
      
      var f = function(){marker.openInfoWindowHtml(
"<div><h2><a href='"+url+"'>"+title+"</a></h2><p>"+content+"</p></div>"
, opt);};
      GEvent.addListener(marker, 'click', f);

    };

    
    
    

    if (typeof(getData) == 'function') {
        var over_obj = getData();
        if (over_obj) {
            for (var i=0; i < over_obj['boxes'].length; i++) registerEventListener(over_obj['boxes'][i], 'click',
                function (){
                    map1.clearOverlays();
                    var bs = getData();
                    for (id in bs) {
                        if (bs[id] == true) {
                            for (var j=0; j < overLays[id].length; j++) {
                                var opts = overLays[id][j];
                                addMarker(opts[0], opts[1], opts[2], opts[3], opts[4], opts[5]);
                            };
                        }
                    };
                });
        }
    };

  }
  else window.alert("Google maps aren't compatible with current browser or your map api key doesn't match your portal root.");
};

registerEventListener(window, 'load', onLoadMap);
registerEventListener(window, 'unload', GUnload);

//]]>
</script>
"""

# Marker testing stuff
MARKER_VIEW_JAVASCRIPT = """
<script type="text/javascript">
//<![CDATA[

function onLoadMap(){
  if (GBrowserIsCompatible()) {

    map1 = new GMap2(document.getElementById('mapView'));
    map1.addControl(new GLargeMapControl());
map1.addControl(new GMapTypeControl());
map1.addControl(new GOverviewMapControl());

    map1.setCenter(new GLatLng(3.500000, 20.400000), 6, G_HYBRID_MAP);
    var opt = map1.getInfoWindow(), overLays = {};
    opt.maxWidth = 400;

    var icon = new GIcon();
    icon.shadow = "http://nohost/plone/images/map_shadow.png";
    icon.iconSize = new GSize(20, 34);
    icon.shadowSize = new GSize(37, 34);
    icon.iconAnchor = new GPoint(9, 34);
    icon.infoWindowAnchor = new GPoint(9, 2);

    function addMarker(lat, lng, title, url, content, col){
      icon.image = "http://nohost/plone/images/"+col+"/map_marker.png";
      var point = new GLatLng(lat, lng);
      var marker = new GMarker(point, icon)
      map1.addOverlay(marker);
      
      var f = function(){marker.openInfoWindowHtml(
"<div><h2><a href='"+url+"'>"+title+"</a></h2><p>"+content+"</p></div>"
, opt);};
      GEvent.addListener(marker, 'click', f);

    };

    
    addMarker(3.500000, 20.400000, "Test Marker", "http://nohost/plone/Members/test_user_1_/test_map/test_marker/view", "Test Marker Description", "default");
    

    if (typeof(getData) == 'function') {
        var over_obj = getData();
        if (over_obj) {
            for (var i=0; i < over_obj['boxes'].length; i++) registerEventListener(over_obj['boxes'][i], 'click',
                function (){
                    map1.clearOverlays();
                    var bs = getData();
                    for (id in bs) {
                        if (bs[id] == true) {
                            for (var j=0; j < overLays[id].length; j++) {
                                var opts = overLays[id][j];
                                addMarker(opts[0], opts[1], opts[2], opts[3], opts[4], opts[5]);
                            };
                        }
                    };
                });
        }
    };

  }
  else window.alert("Google maps aren't compatible with current browser or your map api key doesn't match your portal root.");
};

registerEventListener(window, 'load', onLoadMap);
registerEventListener(window, 'unload', GUnload);

//]]>
</script>
"""