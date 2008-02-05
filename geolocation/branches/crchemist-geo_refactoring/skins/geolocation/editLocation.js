function editLocation(){
  if (GBrowserIsCompatible()) {

    var mapping = {'Map':G_NORMAL_MAP, 'Satellite':G_SATELLITE_MAP,'Hybrid':G_HYBRID_MAP},
        map_t='',
        lat = document.getElementById('latitude'),
        lng = document.getElementById('longitude'),
        lat_el = document.getElementById('maplatitude'),
        lng_el = document.getElementById('maplongitude'),
        map_lat = lat_el.value,
        map_lng = lng_el.value,
        zoom_el = document.getElementById('mapzoom'),
        map_zoom = zoom_el.value,
        map_type = document.getElementsByName('maptype'),
        lat_val = lat.value!=''?lat.value:0,
        lng_val = lng.value!=''?lng.value:0,
        map = new GMap2(document.getElementById('geomap'));

    function validator(a,b){
      if (isNaN(a) || isNaN(b) || a=='' || b=='') return false;
      if (-90<=a && a<=90 && -180<=b && b<=180) return true;
      return false;
    };

    function selectlistener(){
      var z = zoom_el.value!=''?zoom_el.value:6;
      map.setZoom(parseInt(z));
    };
    function fieldlistener(){
      if (validator(lat_el.value, lng_el.value))
        map.setCenter(new GLatLng(parseFloat(lat_el.value), parseFloat(lng_el.value)));
    };
    function boxlistener(){
      var el = window.event?window.event.srcElement:this;
      map.setMapType(mapping[el.value]);
    };
    function addMarker(lat, lng){
      var point = new GLatLng(lat, lng);
      var marker = new GMarker(point)
      map.addOverlay(marker);
    };
    function mapmarkerlistener(marker, point){
      if (!marker){
      map.clearOverlays();
      addMarker(point.y, point.x);
      lat.value = point.y;
      lng.value = point.x;
      }
    };
    function maptypelistener(){document.getElementById(map.getCurrentMapType().getName()).click();};
    function mapzoomlistener(oldzoom, newzoom){zoom_el.selectedIndex = newzoom+1;};
    function mapcenterlistener(){
      lat_el.value = map.getCenter().lat();
      lng_el.value = map.getCenter().lng();
    };

    map.addControl(new GLargeMapControl());
    map.addControl(new GMapTypeControl());
    map.addControl(new GOverviewMapControl());

    for (var i=0; i<map_type.length; i++) {
      if (map_type[i].checked) map_t = map_type[i].value;
      registerEventListener(map_type[i], 'click', boxlistener, false);
    };

    var map_x = map_lat!=''?map_lat:lat_val, map_t,
        map_y = map_lng!=''?map_lng:lng_val,
        map_z = map_zoom!=''?map_zoom:6,
        map_t = map_t=='Map'?G_NORMAL_MAP:map_t=='Satellite'?G_SATELLITE_MAP:G_HYBRID_MAP;

    map.setCenter(new GLatLng(parseFloat(map_x), parseFloat(map_y)), parseInt(map_z), map_t);

    GEvent.addListener(map, 'maptypechanged', maptypelistener);
    GEvent.addListener(map, 'zoomend', mapzoomlistener);
    GEvent.addListener(map, 'moveend', mapcenterlistener);
    GEvent.addListener(map, 'click', mapmarkerlistener);
    addMarker(parseFloat(lat_val), parseFloat(lng_val));

    registerEventListener(zoom_el, 'change', selectlistener, false);
    registerEventListener(lat_el, 'change', fieldlistener, false);
    registerEventListener(lng_el, 'change', fieldlistener, false);

  }
  else window.alert("Google maps aren't compatible with current Browser.");
};

registerPloneFunction(editLocation);
registerEventListener(window, 'unload', GUnload);