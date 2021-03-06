GLOBALS = globals()
PRODUCT_NAME = 'quintagroup.captcha.core'
CAPTCHA_KEY = 'captcha_key'
CAPTCHAS_COUNT = 165

LAYERS = ['captchas', 'captcha_core']
LAYER_DYNAMIC_CAPTCHAS = 'captcha_core/dynamic'
LAYER_STATIC_CAPTCHAS = 'captcha_core/static'
ALL_LAYERS = LAYERS + [LAYER_STATIC_CAPTCHAS, LAYER_DYNAMIC_CAPTCHAS]

#TOOL_ICON = 'tool.gif'
TOOL_ICON = 'skins/captcha_core/tool.gif'
TOOL_ID = 'portal_captchas'
CONFIGLET_ID = "qpc_tool"
PROPERTY_SHEET = 'qPloneCaptchas'

DEFAULT_IMAGE_SIZE = 27
DEFAULT_BG = 'gray'
DEFAULT_FONT_COLOR = 'black'
DEFAULT_PERIOD = 0.1
DEFAULT_AMPLITUDE = 5
DEFAULT_OFFSET = (0.5, 0.5)
DEFAULT_DISTORTION = [DEFAULT_PERIOD, DEFAULT_AMPLITUDE, DEFAULT_OFFSET]
