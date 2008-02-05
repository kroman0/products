# Controller Python Script "save_location"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
#

latitude       = context.REQUEST.get('latitude', 0)
longitude      = context.REQUEST.get('longitude', 0)
maplatitude    = context.REQUEST.get('maplatitude', 0)
maplongitude   = context.REQUEST.get('maplongitude', 0)
mapzoom        = context.REQUEST.get('mapzoom', 0)
maptype        = context.REQUEST.get('maptype', 0)

if not (maplatitude and maplongitude): mapcenter=()
else: mapcenter = (float(maplatitude), float(maplongitude))

context.restrictedTraverse('@@LocationView').editLocation(latitude, longitude)
context.restrictedTraverse('@@MapView').editMapOptions(mapcenter, mapzoom, maptype)

return state.set(portal_status_message="geoLocation property updated")

