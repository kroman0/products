from Products.CMFCore.permissions import View

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import registerATCT

from Products.PloneFormGen.content.fieldsBase import BaseFormField, BaseFieldSchemaStringDefault
from Products.PloneFormGen.content.fields import FGStringField

from Products.qPloneCaptchaField.config import PROJECTNAME
from Products.qPloneCaptchaField.widgets.CaptchaWidget import CaptchaWidget

class CaptchaField(FGStringField):

    schema = BaseFieldSchemaStringDefault

    def __init__(self, oid, **kwargs):
        """ initialize class """

        BaseFormField.__init__(self, oid, **kwargs)

        # set a preconfigured field as an instance attribute
        self.fgField = StringField('fg_string_field',
            searchable=0,
            required=1,
            write_permission = View,
            validators=('isCaptchaCorrect',),
            widget=CaptchaWidget(),
            )

registerATCT(CaptchaField, PROJECTNAME)