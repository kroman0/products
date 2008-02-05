GLOBALS = globals()
PRODUCT_NAME = 'qPloneCaptchas'
CAPTCHAS_COUNT = 165
LAYERS = ['captchas', 'plone_captchas']
LAYER_DISCUSSION = 'captchas_discussion'
LAYER_FORMMAILER = 'captchas_ploneformmailer'
LAYER_DYNAMIC_CAPTCHAS = 'plone_captchas/dynamic'
LAYER_STATIC_CAPTCHAS = 'plone_captchas/static'
ALL_LAYERS = LAYERS + [LAYER_DISCUSSION, LAYER_FORMMAILER, LAYER_STATIC_CAPTCHAS, LAYER_DYNAMIC_CAPTCHAS]
TOOL_ICON = 'tool.gif'
TOOL_ID = 'portal_captchas'
CONFIGLET_ID = "prefs_captchas_setup_form"
CONFIGLET_NAME = "qPloneCaptchas setup"
PROPERTIES = (('static_captchas', 'True', 'boolean'),)

try:
    import PIL
    havePIL = True
except:
    havePIL = False
