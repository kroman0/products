from zope.component import adapts
from zope.interface import implements

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from Products.Archetypes.atapi import RichWidget, ComputedWidget
from Products.Archetypes.public import TextField, ComputedField
from Products.Archetypes.atapi import AnnotationStorage
#from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.interface import IATDocument


from quintagroup.mobileextender import mobileextenderMessageFactory as _


class MobileField(ExtensionField, TextField):
   """A mobile field content mobile version of content."""

class MobileExtender(object):

    fields = [
        MobileField('mobile_content',
                  #required=False,
                  #storage = AnnotationStorage(migrate=True),
                  #default_output_type = 'text/x-html-safe',
                  schemata = 'mobile',
                  default = "",
                  widget = RichWidget(
                            label = _(u'label_mobile_content', default=u'Mobile Content'),
                            rows = 25,
                            allow_file_upload = True),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self): 
        return self.fields

