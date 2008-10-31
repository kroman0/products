from AccessControl import ClassSecurityInfo

from Products.CMFCore.permissions import View
from Products.Archetypes.Field import StringField
from Products.ATContentTypes.content.base import registerATCT

from Products.PloneFormGen.content.fields import FGStringField

from widget import ReadonlyStringWidget
from config import PROJECTNAME

class FGReadonlyStringField(FGStringField):
    """ A string entry field """

    security  = ClassSecurityInfo()

    # Standard content type setup
    portal_type = meta_type = 'FormReadonlyStringField'
    archetype_name = 'Readonly String Field'
    content_icon = 'StringField.gif'
    typeDescription= 'A readonly string field'

    def __init__(self, oid, **kwargs):
        """ initialize class """

        super(FGReadonlyStringField, self).__init__(oid, **kwargs)

        # set a preconfigured field as an instance attribute
        self.fgField = StringField('fg_string_field',
            searchable=0,
            required=0,
            write_permission = View,
            validators=('isNotTooLong',),
            widget=ReadonlyStringWidget(),
            )


registerATCT(FGReadonlyStringField, PROJECTNAME)

