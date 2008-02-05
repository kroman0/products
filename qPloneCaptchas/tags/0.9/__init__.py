from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.utils import ToolInit
from AccessControl import allow_module
import config
import CaptchaTool
allow_module('Products.qPloneCaptchas.utils')
allow_module('Products.qPloneCaptchas.config')

try:
    import PIL
    config.havePIL = True
except:
    config.havePIL = False

registerDirectory('skins', config.GLOBALS)
tools = (CaptchaTool.CaptchaTool, )
def initialize(context):
    ToolInit("PingTool", tools=tools, icon=config.TOOL_ICON).initialize(context)