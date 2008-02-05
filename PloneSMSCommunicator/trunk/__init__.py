# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-12-23 11:54:22
# Copyright: quintagroup.com

"""
This is the init module for PloneSMSCommunicator that will initialize all
types in tool.
"""
__docformat__ = 'restructuredtext'

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
