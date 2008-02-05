## PLONE AND SKIN PRODUCT SPECIFIC CONSTANTS
GLOBALS = globals()
GENERATOR_PRODUCT = "%(GENERATOR_PRODUCT)s"
PRODUCT_NAME = "%(SKIN_PRODUCT_NAME)s"
SKIN_NAME = "%(SKIN_NAME)s"
BASE_SKIN_NAME = "%(BASE_SKIN_NAME)s"


##
## SLOT FORMING CONSTANTS
##
## Skin Product's portlet lists for left and right columns.
## 'None' - mean that on installation slot will not be changed.
## ['some/portlet1','some/portlet2'] - will change appropriate (left or right)
##                                     slot to listed portlets
LEFT_SLOTS = %(LEFT_SLOTS)s
RIGHT_SLOTS = %(RIGHT_SLOTS)s

## Slot's list forming procedure.
## "blend_with_skin" [default]- to SKIN PRODUCT'S slots list added unknown slots from SITE.
## "blend_with_site" - to SITE's slots list added unknown slots from SKIN PRODUCT.
## "replace" - in left and right site's columns placed ONLY SKIN PRODUCT's slots.
#SLOT_FORMING = "blend_with_skin"
#SLOT_FORMING = "blend_with_site"
#SLOT_FORMING = "replace"
SLOT_FORMING = "%(SLOT_FORMING)s"

## Favour column for slots forming procedure. IMPORTANT only for 'Blend with...' 
## Slot's list forming procedure.
## "left" OR "right" - if find same slots in left and right columns - than 
##                     slots move accordingly to left/right column.
## "both" - if find same slots in left and right columns - than slots 
##          positionings as in Master's slots lists - 
##          from SKIN PRODUCT's slots for 'Blend with skin' procedure
##          and SITE's slots for 'Blend with site' one.
#MAIN_COLUMN = "left"
#MAIN_COLUMN = "right"
#MAIN_COLUMN = "both"
MAIN_COLUMN = "%(MAIN_COLUMN)s"


##
## CSS AND JAVASCRIPTS RESOURCES CONSTANTS
## Actual only for 2.1+ Plone. For older Plone version - this data not used.
## Work only if at least one of (DOES_COSTOMIZE_CSS, DOES_COSTOMIZE_JS)
## constant(s) set to True
##
## Does customize CSS or Javascripts resources - define if perform corresponding 
## registry customization.
#DOES_COSTOMIZE_CSS = True # Do portal_css customization
#DOES_COSTOMIZE_CSS = False # Do NOT portal_css customization
DOES_COSTOMIZE_CSS = %(DUMP_CSS)s
#DOES_COSTOMIZE_JS = True # Do portal_javascripts customization
#DOES_COSTOMIZE_JS = False # Do NOT portal_javascripts customization
DOES_COSTOMIZE_JS = %(DUMP_JS)s

## Skin Product's CSS and Javascript lists.
CSS_LIST = %(CSS_LIST)s
JS_LIST = %(JS_LIST)s

## CSS and Javascript registries settings for Skin Product.
## Actual for right functionality css-es and ECMA scripts.
## For manually changing you must know what you do.
SKIN_CSS_REGDATA = %(SKIN_CSS_REGDATA)s
SKIN_JS_REGDATA = %(SKIN_JS_REGDATA)s


##
## IMPORTING OBJECTS TO PORTAL ROOT
##
## *IMPORT_POLICY* define importing behavior in case of presenting identical 
## ids among both - portal root objects and imported objects from 
## <SkinProduct>/import subdirectory.
## "only_new" [default]- imported objects with same ids are ignored - not imported.
## "backup" - in case of presenting same id objects, in portal root creates
##            back_[date] directory, where moved all same id's objects from
##            portal root. Then all objects are imported to portal root.
## "overwrite" - all objects in portal root with same ids are deleted. Then all 
##               objects are imported to portal root.
#
#IMPORT_POLICY = "backup"
#IMPORT_POLICY = "overwrite"
#IMPORT_POLICY = "only_new"
IMPORT_POLICY = "%(IMPORT_POLICY)s"


##
## CUSTOMIZATION FUNCTIONS
##
## FINAL_CUSTOMIZATION_FUNCTIONS - list of additional customization functions.
## For perform additional customization in the SkinProduct - write in this config.py
## module a customization function(s) and add its name(s) to FINAL_CUSTOMIZATION_FUNCTIONS
## constant list. Customization function must acept 2 parameters: 'portal' and 'out'.
## Example:    
## def myCustomization(portal, out):
##     # Clear right slots for portal
##     portal.manage_addProperty('my_prop', 'my_value', type='string')
##     print >> out, "right slots deleted for portal."
## FINAL_CUSTOMIZATION_FUNCTIONS = [myCustomization]
from Products.CMFCore.utils import getToolByName
FINAL_CUSTOMIZATION_FUNCTIONS = []
