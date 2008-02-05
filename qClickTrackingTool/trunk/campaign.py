from Products.Archetypes.public import *
from config import *

schema = BaseSchema+Schema((
                             TextField('description',
                                        accessor = "Description",
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
    archetype_name = TYPE_TITLE
    _at_rename_after_creation = True

registerType(campaign)