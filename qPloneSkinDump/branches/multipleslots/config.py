import re, os
from Products.CMFCore import CMFCorePermissions

## Base Product Constants
GLOBALS = globals()
PROJECTNAME = "qPloneSkinDump"
ADD_CONTENT_PERMISSION = CMFCorePermissions.AddPortalContent
CONFIGURATION_CONFIGLET = "qploneskindump_configuration"

## Name for mian_template generation configlet
GENERATION_CONFIGLET = "qploneskindump_generation"


## Constants for Scin Product generation
TEMPLATE_PATH = "skin_template"


## Constants for slots castomization
SLOT_FORMING_LIST = ["blend_with_skin", "blend_with_site", "replace"]
DEFAULT_SLOT_FORMING = "blend_with_skin"
MAIN_COLUMN_LIST = ["left", "right", "both"]
DEFAULT_MAIN_COLUMN = "both"


## Constants for Exporting objects
IMPORTING_POLICY_LIST = ["only_new","backup","overwrite"]
DEFAULT_IMPORTING_POLICY = "only_new"
FORBIDDEN_EXP_PREFIXES = re.compile('^(portal_)')
FORBIDDEN_EXP_NAMES = ["MailHost", "HTTPCache", "Members", "RAMCache", "acl_users",\
                       "archetype_tool", "caching_policy_manager", "content_type_registry", \
                       "cookie_authentication", "error_log", "kupu_library_tool",\
                       "mimetypes_registry", "plone_utils", "reference_catalog",\
                       "translation_service", "uid_catalog"]


## Resource registries proprties
CSS_REG_PROPS = ['id', 'expression', 'enabled', 'cookable', 'cacheable' \
                ,'media', 'rel', 'title', 'rendering', 'compression']
JS_REG_PROPS = ['id', 'expression', 'enabled', 'cookable', 'cacheable' \
               ,'inline', 'compression']


from Globals import package_home
PRODUCTS_PATH = os.sep.join(package_home(GLOBALS).split(os.sep)[:-1])

import Products
from OFS.Application import get_products
