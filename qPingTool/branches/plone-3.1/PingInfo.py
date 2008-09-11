from Globals import DTMLFile
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFDefault.utils import _dtmldir
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema, finalizeATCTSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from config import RSS_LIST, PROJECTNAME

PingInfoSchema =  ATContentTypeSchema.copy() +  Schema((
    TextField('description',
        default = '',
        searchable = 0,
        widget = TextAreaWidget(
            label_msgid = 'label_description',
            description_msgid = 'help_description',),
               ),
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
		default='Weblog',
                widget=SelectionWidget(label_msgid = 'label_rss_version',
                                    description_msgid = 'help_rss_version'),
    )),
    marshall=RFC822Marshaller()
    )
    
finalizeATCTSchema(PingInfoSchema)

class PingInfo(ATCTContent, HistoryAwareMixin):
    """Ping Info container
       id - name of the server to ping
       url - server ping url
       method_name - ping method
       rss_version - rss version supported by the server
    """
    __implements__ = (ATCTContent.__implements__,
                      HistoryAwareMixin.__implements__,
                     )
    schema = PingInfoSchema

    """
        Added some support of DublinCore
    """
    security = ClassSecurityInfo()

    def Contributors(self):
        return self.contributors

    security.declareProtected(ModifyPortalContent, 'manage_metadata' )
    manage_metadata = DTMLFile('zmi_metadata', _dtmldir)


registerType(PingInfo, PROJECTNAME)
