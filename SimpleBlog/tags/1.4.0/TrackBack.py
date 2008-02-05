from Products.Archetypes.public import *
#from Products.Archetypes.BaseContent import BaseContent
from config import *

schema = BaseSchema +  Schema((
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


class TrackBack(BaseContent):
    """Track Back Info container
       title - title of track Back
       url - server ping url
       blog_name - blog-sender name 
       excerpt - simplified content text
    """
    schema = schema

    # Override original ExtensibleMetadata method
    # for prevent "Unauthorized" exception raicing
    def allowDiscussion(self, allowDiscussion=None, **kw):
        """ """
        return None


registerType(TrackBack) 