## Script (Python) "view_js"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= result=None
##title=
##

map_center = (0,0)
sMarker = ""
if result:
    map_center = result
    sMarker = """
var point = new GLatLng(parseFloat(%f), parseFloat(%f));
var marker = new GMarker(point);
map2.addOverlay(marker);""" % (map_center[0], map_center[1])

return """
<script src="http://maps.google.com/maps?file=api&v=2&key=%(key)s" type="text/javascript"></script>
<script type="text/javascript">
//<![CDATA[

function onMapLoad() {
    if (GBrowserIsCompatible()) {
        var map2 = new GMap2(document.getElementById("mapView"));
        map2.addControl(new GLargeMapControl());
        map2.addControl(new GMapTypeControl());
        map2.addControl(new GOverviewMapControl());
        map2.setCenter(new GLatLng(%(lat)f, %(lng)f), 6, G_HYBRID_MAP);
        %(marker)s
    }
    else window.alert("Google maps aren't compatible with current Browser.");
}

registerEventListener(window, 'load', onMapLoad)
registerEventListener(window, 'unload', GUnload);

//]]>
</script> """ % {
                 'key'      : context.getMapKey(),
                  'lat'     : map_center[0],
                  'lng'     : map_center[1],
                  'marker'  : sMarker,
                }