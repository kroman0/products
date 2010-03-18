from zope.i18nmessageid import MessageFactory

from AccessControl import allow_module, ModuleSecurityInfo

from quintagroup.plonecaptchas import config

ProductMessageFactory = MessageFactory('quintagroup.plonecaptchas')
ModuleSecurityInfo('quintagroup.plonecaptchas').declarePublic("ProductMessageFactory")

allow_module('quintagroup.plonecaptchas.config')

def initialize(context):
    pass