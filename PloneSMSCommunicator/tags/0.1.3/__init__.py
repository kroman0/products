from Products.CMFCore.DirectoryView import registerDirectory
from Products.Archetypes.public import *
from AccessControl import allow_module
from Products.CMFCore import utils

from PloneSMSCommunicator import PloneSMSCommunicator
from config import *

registerDirectory(SKINS_DIR, GLOBALS)

tools=(PloneSMSCommunicator,)

allow_module('Products.PloneSMSCommunicator.Utils')
allow_module('Products.PloneSMSCommunicator.config')

def initialize(context):
    utils.ToolInit(PROJECTNAME,
                   tools=tools,
                   product_name=PROJECTNAME,
                   icon= "tool.gif",
                  ).initialize(context)
