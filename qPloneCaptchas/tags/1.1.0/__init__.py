from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.utils import ToolInit
from AccessControl import allow_module
import config
import CaptchaTool

allow_module('Products.qPloneCaptchas.utils')
allow_module('Products.qPloneCaptchas.config')
registerDirectory('skins', config.GLOBALS)

tools = (CaptchaTool.CaptchaTool, )
def initialize(context):
    ToolInit(meta_type="CaptchaTool",
             tools=tools,
             product_name=config.PRODUCT_NAME,
             icon=config.TOOL_ICON,).initialize(context)
