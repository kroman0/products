from Products.Archetypes.public import *
from Products.Archetypes.BaseContent import BaseContentMixin
from Products.CMFCore.ActionInformation import ActionInformation
from Products.CMFCore.Expression import Expression, createExprContext
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner, aq_parent
from config import *

schema = BaseContentMixin.schema +  Schema((
    #StringField('id',
    #            required=1,
    #            widget=StringWidget(size=70,
    #                                label_msgid = 'label_id',
    #                                description_msgid = 'help_id'),
    #            ),
    StringField('url',
                required=1,
                widget=StringWidget(label_msgid = 'label_url',
                                    description_msgid = 'help_url'),
               ),
    StringField('method_name',
                default='weblogUpdates.ping',
                required=1,
                widget=StringWidget(label_msgid = 'label_method_name',
                                    description_msgid = 'help_method_name'),
               ),
    StringField('rss_version',
		vocabulary=RSS_LIST,
		default='Blog',
                widget=SelectionWidget(label_msgid = 'label_rss_version',
                                    description_msgid = 'help_rss_version'),
                ),
    ))


class PingInfo(BaseContentMixin):
    """Ping Info container
       id - name of the server to ping
       url - server ping url
       method_name - ping method
       rss_version - rss version supported by the server
    """ 
    schema = schema

registerType(PingInfo)