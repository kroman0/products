from ZPublisher import HTTPRequest
from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerField, registerWidget


class MapWidget(TypesWidget):

    _properties = TypesWidget._properties.copy()
    _properties.update({
        'type': 'map',
        'macro': 'map_widget',
    })

    security = ClassSecurityInfo()

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None, emptyReturnsMarker=False):
        """ create tuple from latitude and longitude """
        latitude = form.get('%s_latitude' % field.getName(), empty_marker)
        longitude = form.get('%s_longitude' % field.getName(), empty_marker)
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except: pass
        return (latitude, longitude),  {}


class MapField(atapi.ObjectField):

    _properties = atapi.ObjectField._properties.copy()
    _properties.update({
        'widget'  : MapWidget,
        'default' : None,
    })

registerWidget(
    MapWidget,
    title='Map Coordinates',
    used_for=('Products.field.MapField',)
    )

registerField(
    MapField,
    title="MapField",
    description=("Field that can store coordinate information (longitude, latitude)"
                 "on the map")
    )