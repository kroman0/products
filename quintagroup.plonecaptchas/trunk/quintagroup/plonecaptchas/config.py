GLOBALS = globals()
PRODUCT_NAME = 'quintagroup.plonecaptchas'
CAPTCHAS_COUNT = 165

LAYERS = ['captchas', 'plone_captchas', 'captchas_discussion', 
    'captchas_sendto_form', 'captchas_join_form']
LAYER_DYNAMIC_CAPTCHAS = 'plone_captchas/dynamic'
LAYER_STATIC_CAPTCHAS = 'plone_captchas/static'
ALL_LAYERS = LAYERS + [LAYER_STATIC_CAPTCHAS, LAYER_DYNAMIC_CAPTCHAS]

TOOL_ICON = 'tool.gif'
TOOL_ID = 'portal_captchas'
CONFIGLET_ID = "prefs_captchas_setup_form"
CONFIGLET_NAME = "qPloneCaptchas setup"

DEFAULT_IMAGE_SIZE = 27
DEFAULT_BG = 'gray'
DEFAULT_FONT_COLOR = 'black'
DEFAULT_PERIOD = 0.1
DEFAULT_AMPLITUDE = 5
DEFAULT_OFFSET = (0.5, 0.5)
DEFAULT_DISTORTION = [DEFAULT_PERIOD, DEFAULT_AMPLITUDE, DEFAULT_OFFSET]

PROPERTIES = (('image_size', DEFAULT_IMAGE_SIZE, 'int'),
              ('background', DEFAULT_BG, 'string'),
              ('font_color', DEFAULT_FONT_COLOR, 'string'),
              ('period', DEFAULT_PERIOD, 'float'),
              ('amplitude', DEFAULT_AMPLITUDE, 'float'),
              ('random_params', True, 'boolean'))
