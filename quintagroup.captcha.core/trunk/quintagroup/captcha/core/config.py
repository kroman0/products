GLOBALS = globals()
PRODUCT_NAME = 'quintagroup.captcha.core'
CAPTCHA_KEY = 'captcha_key'
CAPTCHAS_COUNT = 165

LAYERS = ['captchas', 'plone_captchas', 'captchas_discussion', 
    'captchas_sendto_form', 'captchas_join_form']
LAYER_DYNAMIC_CAPTCHAS = 'plone_captchas/dynamic'
LAYER_STATIC_CAPTCHAS = 'plone_captchas/static'
ALL_LAYERS = LAYERS + [LAYER_STATIC_CAPTCHAS, LAYER_DYNAMIC_CAPTCHAS]

#TOOL_ICON = 'tool.gif'
TOOL_ICON = 'skins/plone_captchas/tool.gif'
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
