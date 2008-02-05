#from AccessControl import allow_module

#allow_module('Products.qMemberdataExport.MemberdataHandlers')

from MemberdataHandlers import getRegisteredMemberdataHandlers

# import BaseMemberdataHandler first for registering it as last (default) in list of all registered handlers

from BaseMemberdataHandler import BaseMemberdataHandler
from CMFMemberdataHandler import CMFMemberdataHandler
from PASMemberdataHandler import PASMemberdataHandler
from RememberMemberdataHandler import RememberMemberdataHandler