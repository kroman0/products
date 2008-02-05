from Products.Archetypes.public import *
from config import *

schema=BaseFolderSchema 

def modify_fti(fti):
        fti['allowed_content_types'] = ('Campaign')
        fti['filter_content_types'] = 1
        fti['global_allow']=0
        actions = fti['actions']
        for a in actions:
            if a['id'] == 'view':
                a['action'] = 'string:${object_url}/portal_clicktracker_view'
        actions = list(actions)

        fti['actions']=tuple(actions)

class ClickTracker(BaseFolder):

    schema=schema
    archetype_name=PROJECTNAME
    id=TOOLID

    def __init__(self):
        BaseFolder.__init__(self, self.id)

registerType(ClickTracker)