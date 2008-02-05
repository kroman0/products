## Script (Python) "qploneskindump_config_script"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##

#from Products.CMFCore.utils import getToolByName
from Products.qPloneSkinDump.qPloneSkinDump import createProduct
from Products.CMFPlone import PloneMessageFactory as _

REQUEST = context.REQUEST
# ZMI data
zmi_skin_names = REQUEST.get('ZMISkinName')
zmi_base_skin_name = REQUEST.get('ZMIBaseSkinName')

# File system data
fs_skin_directory = REQUEST.get('FSSkinDirectory')
fs_product_name = REQUEST.get('FSProductName')
erase_from_skin = REQUEST.get('EraseFromSkin')

# Slots customization data
left_slots = right_slots = slot_forming = main_column = None
doesCustomizeSlots = REQUEST.get('DoesCustomizeSlots')
if doesCustomizeSlots:
    slot_forming = REQUEST.get('slot_forming')
    main_column = REQUEST.get('main_column')

    left_slots = REQUEST.get('left_slots')
    right_slots = REQUEST.get('right_slots')
    if left_slots:
        left_slots = [i for i in left_slots if i]
    if right_slots:
        right_slots = [i for i in right_slots if i]

# Exporting portlets
dump_portlets = REQUEST.get('dump_portlets', 0)
dump_policy = REQUEST.get('dump_policy', 'root')
dump_portlets_selection = REQUEST.get('dump_objects', [])

# Exporting objects
import_policy = exporting_objects = None
doesExportObjects = REQUEST.get('DoesExportObjects')
if doesExportObjects:
    import_policy = REQUEST.get('import_policy')
    exporting_objects = REQUEST.get('exporting_objects')
#return [doesExportObjects, import_policy, exporting_objects]

# Exporting portal resources
dump_CSS = dump_JS = None
dump_CSS = REQUEST.get('DumpCSSRegistry')
dump_JS = REQUEST.get('DumpJSRegistry')

dump_custom_views = REQUEST.get('dump_viewlets', None)

# create Product
result = createProduct(context, zmi_skin_names=zmi_skin_names,\
              zmi_base_skin_name=zmi_base_skin_name,\
              fs_skin_directory=fs_skin_directory,\
              fs_product_name=fs_product_name,\
              erase_from_skin=erase_from_skin,\
              doesCustomizeSlots=doesCustomizeSlots,\
              left_slots=left_slots,\
              right_slots=right_slots,\
              slot_forming=slot_forming,\
              main_column=main_column,
              doesExportObjects=doesExportObjects,\
              import_policy=import_policy,\
              exporting_objects=exporting_objects, \
              dump_CSS=dump_CSS, \
              dump_JS=dump_JS, \
              dump_portlets=dump_portlets, \
              dump_policy=dump_policy,
              dump_portlets_selection=dump_portlets_selection,
              dump_custom_views=dump_custom_views)

portal_status_message = u'"%s" Product successfully created.' % fs_product_name
if result:
    portal_status_message = portal_status_message + u"Failed exporting objects: %s." % str(result)

context.plone_utils.addPortalMessage(_(portal_status_message))
return state
