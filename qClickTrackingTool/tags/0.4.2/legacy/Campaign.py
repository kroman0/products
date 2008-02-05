from Products.Archetypes.public import *
from Products.CMFDefault.Link import Link
from Products.ATContentTypes.types.ATLink import ATLink
from Products.qClickTrackingTool.config import *


class Campaign(ATLink):
    """My own link based on ATLink"""

    schema         =  ATLink.schema
    meta_type      = 'Campaign'
    archetype_name = 'Campaign'

    __implements__ = ATLink.__implements__

registerType(Campaign, PROJECTNAME)
