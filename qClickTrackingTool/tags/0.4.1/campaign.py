from Products.Archetypes.public import *
from config import *

schema = BaseSchema+Schema((
                             TextField('description',
                                        widget = TextAreaWidget(
                                                                description = "Enter your description.",
                                                                label="Description"
                                                               ),
                                      ),
                             StringField('url',
                                         default = "http://",
                                         validators = ('isURL',),
                                         widget = StringWidget(
                                                                description = "Url address of your campaign location",
                                                               ),
                                        ),
                          ))

def modify_fti(fti):
    fti['content_icon'] = 'link_icon.gif'

class campaign(BaseContent):

    schema=schema
    archetype_name = TYPE_NAME

registerType(campaign)