## Script (Python) "edit_js"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= result=None, longlat=[]
##title=
##

lat = []
lon = []
map_center = (0,0)
sMarker = ""
sGlobVars = "var autoZoom=null, autoCenter=null;"

if longlat:
    lat = [float(e.geoLocation[0]) for el in longlat.values() for e in el]
    lon = [float(e.geoLocation[1]) for el in longlat.values() for e in el]

if lat and lon:
    sGlobVars = """
autoCenter = [%f, %f];
autoZoom = map3.getBoundsZoomLevel(new GLatLngBounds(new GLatLng(%f, %f), new GLatLng(%f, %f)));""" % ((min(lat)+max(lat))/2, (min(lon)+max(lon))/2, min(lat), min(lon), max(lat), max(lon))

if result:
    map_center = (float(result[0]), float(result[1]))
    sMarker = """
var point = new GLatLng(parseFloat(%f), parseFloat(%f));
var marker = new GMarker(point);
map3.addOverlay(marker);""" % (map_center[0], map_center[1])

return """
<script src="http://maps.google.com/maps?file=api&v=2&key=%(key)s" type="text/javascript"></script>
<script type="text/javascript">
//<![CDATA[

function onMapLoad() {
    if (GBrowserIsCompatible()) {
        var lat = document.getElementById("maplatitude"),
            lng = document.getElementById("maplongitude"),
            map3 = new GMap2(document.getElementById("mapView"));
        this.mp = map3;
        map3.addControl(new GLargeMapControl());
        map3.addControl(new GMapTypeControl());
        map3.addControl(new GOverviewMapControl());
        map3.setCenter(new GLatLng(parseFloat(%(lat)f), parseFloat(%(lng)f)), 6, G_HYBRID_MAP);
        %(globvars)s
        %(marker)s

        function addMarker(lat, lng){
          var point = new GLatLng(lat, lng);
          var marker = new GMarker(point)
          map3.addOverlay(marker);
        };

        GEvent.addListener(map3, 'click', function(marker, point) {
          if (!marker){
            map3.clearOverlays();
            addMarker(point.y, point.x);
            lat.value = point.y;
            lng.value = point.x;
          }
        });
        return {'widgetMap':map3, 'autoZoom':autoZoom, 'autoCenter':autoCenter};
    }
    else {
        window.alert("Google maps aren't compatible with current Browser.");
        return null;
    }
}

var globMap = onMapLoad();

registerEventListener(window, 'unload', GUnload);

//]]>
</script> """ % {
                 'key'       : context.getMapKey(),
                  'lat'      : map_center[0],
                  'lng'      : map_center[1],
                  'marker'   : sMarker,
                  'globvars' : sGlobVars
                }