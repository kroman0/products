## Script (Python) "getCenterZoom"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

return """
<script type="text/javascript">
//<![CDATA[

var node = document.getElementById('autozoom');
if ((globMap != null) && (globMap.autoCenter != null)) {
  var lt = globMap.autoCenter[0],
      lg = globMap.autoCenter[1];
  if ((lt != null) && (lg != null)) {
    function forLink() {
      globMap.widgetMap.clearOverlays();
      globMap.widgetMap.addOverlay(new GMarker(new GLatLng(parseFloat(lt),parseFloat(lg))));
      globMap.widgetMap.panTo(new GLatLng(parseFloat(lt),parseFloat(lg)));
      var lat = document.getElementById("maplatitude"),
          lng = document.getElementById("maplongitude");
      lat.value = parseFloat(lt);
      lng.value = parseFloat(lg);
      return false;
    };
    node.innerHTML  = "<a href='#' onclick='javascript:forLink();return false;'>Auto Center</a>";
}};

registerEventListener(window, 'unload', GUnload);

//]]>
</script>
"""