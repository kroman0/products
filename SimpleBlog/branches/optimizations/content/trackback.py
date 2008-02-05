from Products.Archetypes.public import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
#from Products.Archetypes.BaseContent import BaseContent
#from Products.SimpleBlog.config import *

schema = ATContentTypeSchema.copy() + Schema((
#schema = BaseSchema +  Schema((
    StringField('url',
                widget=StringWidget(label_msgid = 'label_url',
                                    description_msgid = 'help_url'),
               ),
    StringField('blog_name',
                widget=StringWidget(label_msgid = 'label_blog_name',
                                    description_msgid = 'help_blog_name'),
               ),
    TextField('excerpt',
               widget = RichWidget(label = "excerpt",
                                  label_msgid = "label_excerpt",
                                  i18n_domain = "plone")),
    ))

class TrackBack(ATCTContent):
    """Track Back Info container
       title - title of track Back
       url - server ping url
       blog_name - blog-sender name 
       excerpt - simplified content text
    """
    # Standard content type setup
    portal_type = meta_type = archetype_name = 'TrackBack'
    #content_icon='entry_icon.gif'
    global_allow=1                          ## Change to 0 !!!
    allow_discussion = 0

    default_view = 'base_view'
    immediate_view = 'base_view'

    # Make sure we get title-to-id generation when an object is created
    _at_rename_after_creation = False

    def canSetDefaultPage(self):
        return False

    schema = schema
    # Override original ExtensibleMetadata method
    # for prevent "Unauthorized" exception raicing
    def allowDiscussion(self, allowDiscussion=None, **kw):
        """ """
        return None

registerType(TrackBack)