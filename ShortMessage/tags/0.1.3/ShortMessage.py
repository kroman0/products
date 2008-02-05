from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import *

from validators import MaxSmValidator
from config import *

schema = BaseSchema+Schema((
                    ComputedField('title',
		                  accessor = 'Title',
           	                  expression = "context.getBody()[:25]+'...'",
				  widget=ComputedWidget(
				  visible={'edit':'invisible',
				           'view':'invisible'}, ),
             	   		           ),
		    StringField('sender',
			        required=1,
                                default_method = 'setDefaultSender',
                                widget = StringWidget(
                                condition = "python: object.portal_smsCommunicator.getProperty('policy') == 'free'"
                                                      )
				 ),
		    StringField('recipient',
                                 required=1,
                                 widget = LinesWidget(
                                          rows = 1,
                                          label="recipient"),
                                           ),
                     TextField('body',
		                searchable = 1,
				validators=MaxSmValidator(),
                                widget = TextAreaWidget(
                                         description = "Enter your text message.",
                                         label = "Body text")
			                   ),
                           ))

class ShortMessage(BaseContent):

    schema = schema
    archetype_name=ARCHETYPE_NAME

    def setDefaultSender(self):
        communicator = getToolByName(self, 'portal_smsCommunicator')
        policy = communicator.getProperty('policy')
        if policy == 'free':
            return None
        else:
            return communicator.getProperty('mtMessageOriginator')

registerType(ShortMessage)