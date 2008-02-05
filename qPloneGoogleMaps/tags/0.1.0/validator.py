from Products.validation.interfaces import ivalidator

class MapFieldValidator:

    __implements__ = (ivalidator,)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if value == None: return 1
        if value == ('', ''): return """ This field is required. """
        try:
            lat, lng = value
        except: return """ Validation failed. Unexpected field value. """
        try:
            lat = float(lat)
            lng = float(lng)
        except: return """ Validation failed. Coordinates must be an decimal numbers. """
        if not (-90  <= lat <= 90 ): return """ Validation failed. Latitude not in bounds [-90, 90]. """
        if not (-180 <= lng <= 180): return """ Validation failed. Longitude not in bounds [-180, 180]. """
        return 1