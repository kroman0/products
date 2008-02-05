## Script (Python) "maps_markers"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= longlat=[], node, controls='nothing', maptype='hybrid', overviewControls=None, typeControls=None, events=False, color='default', zoom=None, loc=(37.4419, -122.1419), mapevents=None, auto='Full'
##title=
##

from Products.qPloneGoogleMaps.utility import processDesc

lon = []
lat = []
sPortal = context.portal_url()
sControls = ""
sMarkerEvents = ""
sMapEvents = ""
sDefaults = ""
sMarkers = ""
sInfoWindow = """
"<div><h2><a href='"+url+"'>"+title+"</a></h2><p>"+content+"</p></div>"
"""
sMarkerForm = """
"<input name='markertitle' type='text' value='' /><br /><input name='ok' type='button' value='OK' /><input name='cancel' type='button' value='CANCEL' />"
"""

if maptype == 'satellite': maptype = 'G_SATELLITE_MAP'
elif maptype == 'map': maptype = 'G_NORMAL_MAP'
else: maptype = 'G_HYBRID_MAP'

if (not color) and longlat:
    lat = [float(e.geoLocation[0]) for el in longlat.values() for e in el]
    lon = [float(e.geoLocation[1]) for el in longlat.values() for e in el]
    sMarkers = "\n".join(["""
addMarker(%(lt)f, %(lg)f, "%(title)s", "%(url)s/view", "%(desc)s", "%(c)s");
typeof(overLays["%(id)s"])=='undefined'?overLays["%(id)s"]=[]:'';
overLays["%(id)s"].push([%(lt)f, %(lg)f, "%(title)s", "%(url)s/view", "%(desc)s", "%(c)s"]);
""" % {'lt':float(e.geoLocation[0]),
       'lg':float(e.geoLocation[1]),
       'title':e.Title,
       'url':e.getURL(),
       'desc':processDesc(e.Description),
       'c':el[1],
       'id':el[0]} for el, value in longlat.items() for e in value])
elif longlat:
    lat = [float(el.geoLocation[0]) for el in longlat]
    lon = [float(el.geoLocation[1]) for el in longlat]
    sMarkers = "\n".join(["""addMarker(%f, %f, "%s", "%s/view", "%s", "%s");""" % (float(el.geoLocation[0]), float(el.geoLocation[1]), el.Title, el.getURL(), processDesc(el.Description), color) for el in longlat])

if controls == 'large': sControls += "map1.addControl(new GLargeMapControl());\n"
elif controls == 'small': sControls += "map1.addControl(new GSmallMapControl());\n"
if typeControls: sControls += "map1.addControl(new GMapTypeControl());\n"
if overviewControls: sControls += "map1.addControl(new GOverviewMapControl());\n"

#if mapevents:
if False:
    sMapEvents = """
      var listener = function(marker, point) {
          if (!marker){
            var m = new GMarker(point);
            map1.addOverlay(m);
            m.openInfoWindowHtml(%s);
            var ok_buttons = document.getElementsByName('ok');
            var c_buttons = document.getElementsByName('cancel');
            for (var i=0; i < ok_buttons.length; i++) {
                ok_buttons[i].addEventListener('click', function(){map1.closeInfoWindow()}, false);
                c_buttons[i].addEventListener('click', function(){map1.closeInfoWindow();map1.removeOverlay(m);}, false);
                GEvent.addEvent(m, 'infowindowclose', function(){map1.removeOverlay(m);}, false);
            };
            //map1.removeOverlay(m);
            infowindow = map1.getInfoWindow();
            infowindow.reset(point);
            //window.alert(infowindow instanceof null);
            //GEvent.addListener(infowindow, 'closeclick', function(){map1.removeOverlay(m)});
        }
      };
      GEvent.addListener(map1, 'click', listener);""" % sMarkerForm

if events:
    sMarkerEvents = """
      var f = function(){marker.openInfoWindowHtml(%s, opt);};
      GEvent.addListener(marker, 'click', f);\n""" % sInfoWindow

if lon and lat and auto != 'None':
    sDefaults = """
var centerPoint = new GLatLng(%f, %f),
autoZoom = map1.getBoundsZoomLevel(new GLatLngBounds(new GLatLng(%f, %f), new GLatLng(%f, %f)));
""" % ((min(lat)+max(lat))/2, (min(lon)+max(lon))/2, min(lat), min(lon), max(lat), max(lon))
    if auto == 'Zoom': sDefaults += """map1.setZoom(autoZoom);"""
    elif auto == 'Center': sDefaults += """map1.setCenter(centerPoint);"""
    elif auto == 'Full': sDefaults += """map1.setCenter(centerPoint, autoZoom);"""
    sDefaults += """map1.savePosition();"""

if not zoom: zoom = 6

return """
<script type="text/javascript">
//<![CDATA[

function onLoadMap(){
  if (GBrowserIsCompatible()) {

    map1 = new GMap2(document.getElementById('%(node)s'));
    %(controls)s
    map1.setCenter(new GLatLng(%(lt)f, %(ln)f), %(zoom)s, %(maptype)s);
    var opt = map1.getInfoWindow(), overLays = {};
    opt.maxWidth = 400;

    var icon = new GIcon();
    icon.shadow = "%(url)s/images/map_shadow.png";
    icon.iconSize = new GSize(20, 34);
    icon.shadowSize = new GSize(37, 34);
    icon.iconAnchor = new GPoint(9, 34);
    icon.infoWindowAnchor = new GPoint(9, 2);

    function addMarker(lat, lng, title, url, content, col){
      icon.image = "%(url)s/images/"+col+"/map_marker.png";
      var point = new GLatLng(lat, lng);
      var marker = new GMarker(point, icon)
      map1.addOverlay(marker);
      %(event)s
    };

    %(mapevents)s
    %(markers)s
    %(defaults)s

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
""" % {
   'url'       : sPortal,
   'node'      : node,
   'markers'   : sMarkers,
   'defaults'  : sDefaults,
   'controls'  : sControls,
   'event'     : sMarkerEvents,
   'mapevents' : sMapEvents,
   'zoom'      : zoom,
   'lt'        : float(loc[0]),
   'ln'        : float(loc[1]),
   'maptype'   : maptype}