from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender

from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import MultiSelectionWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import DisplayList

class ExtendableStringField(ExtensionField, StringField):
    """An extendable string field."""

class ExtendableLinesField(ExtensionField, LinesField):
    """An extendable string field."""

access_lst = ("", "Subscription", "Registration")
genres_lst = ("", "PressRelease","Satire","Blog","OpEd","Opinion","UserGenerated")

class NewsExtender(object):
    implements(ISchemaExtender)

    fields = [
        ExtendableStringField("gsm_access",
            accessor="gsm_access",
            vocabulary=DisplayList(zip(access_lst, access_lst)),
            default="",
            schemata="GoogleSitemap",
            widget = SelectionWidget(
                label="Access",
                description="Specifies whether an article is available to all " \
                    "readers (in case of the emtpy field, or only to those " \
                    "with a free or paid membership to your site.",
                format="radio"),
        ),
        ExtendableLinesField("gsm_genres",
            accessor="gsm_genres",
            vocabulary=DisplayList(zip(genres_lst, genres_lst)),
            schemata="GoogleSitemap",
            default=(),
            widget = MultiSelectionWidget(
                label="Genres",
                description="Select one or more properties for an article, " \
                    "namely, whether it is a press release, a blog post, an " \
                    "opinion, an op-ed piece, user-generated content, or satire.",
                format="checkbox"),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
