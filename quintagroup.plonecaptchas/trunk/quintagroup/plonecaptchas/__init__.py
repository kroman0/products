import logging

from App.version_txt import getZopeVersion
from AccessControl import allow_module, ModuleSecurityInfo

from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.utils import ToolInit

import config
import CaptchaTool

allow_module('quintagroup.plonecaptchas.utils')
allow_module('quintagroup.plonecaptchas.config')
registerDirectory('skins', config.GLOBALS)

tools = (CaptchaTool.CaptchaTool, )
def initialize(context):
    ToolInit(meta_type="CaptchaTool",
             tools=tools,
             icon=config.TOOL_ICON,).initialize(context)

def MessageFactory(projectname):
    "Get a i18n message factory"
    MessageFactory = lambda x: lambda y: y
    try: # for Zope3 and Zope 2.9
        from zope.i18nmessageid import MessageFactory
    except ImportError:
        try: # for Zope 2.8
            from zope.i18nmessageid import MessageIDFactory as MessageFactory
        except ImportError:
            try: # for zope 2.7
               from Products.PlacelessTranslationService.MessageID import MessageIDFactory as MessageFactory
            except:
               logging.info("[qPloneCaptchas] No i18n Message Factory found -> cannot provide translations!")
    return MessageFactory(projectname.lower())

ProductMessageFactory = MessageFactory('%s' % config.PRODUCT_NAME)
ModuleSecurityInfo('Products.%s' % config.PRODUCT_NAME).declarePublic("ProductMessageFactory")
