# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-11-23 12:57:23 +0200 (Thu, 23 Nov 2005) $
# Copyright: quintagroup.com

"""ShortMessage is Archetypes-based content type. It has Workflow that sends Short message upon object publishing.
   This module defines the following classes:

    - `ShortMessage`, a ShortMessage type that allows you to create your own short message
   Methods:
    - `ShortMessage.setDefaultSender`: sets none to Sender field if policy is free and enforceOriginator in other case"""

__docformat__ = 'restructuredtext'

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
    """ShortMessage type allows you to create your own short message"""
    schema = schema
    archetype_name=ARCHETYPE_NAME

    def setDefaultSender(self):
        """ sets none to Sender field if policy is free and enforceOriginator in other case"""
        communicator = getToolByName(self, 'portal_smsCommunicator')
        policy = communicator.getProperty('policy')
        if policy == 'free':
            return None
        else:
            return communicator.getProperty('mtMessageOriginator')

registerType(ShortMessage)