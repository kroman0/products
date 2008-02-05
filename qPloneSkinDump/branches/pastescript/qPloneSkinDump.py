import os, re
from AccessControl import ModuleSecurityInfo
from Products.CMFCore.utils import getToolByName

from config import *
from utils import *
from exportingObjects import exportObjects

security = ModuleSecurityInfo( 'Products.qPloneSkinDump.qPloneSkinDump' )

security.declarePublic('getExportingData')
def getExportingData(context):
    result_list = { 'default_import_policy':DEFAULT_IMPORTING_POLICY
                   ,'import_policy_list':{}
                   ,'export_object_id_list':[] }
    # Form allowed id list for exporting
    portal_ids = getToolByName(context, 'portal_url').getPortalObject().objectIds()
    result_list['export_object_id_list'] = [id for id in portal_ids \
                                            if id not in FORBIDDEN_EXP_NAMES \
                                            and not FORBIDDEN_EXP_PREFIXES.match(id)]
    # Form importing_policy_list dictionary with readable names
    result_list['import_policy_list'] = ipols = {}
    [ipols.update({ip:ip.replace("_"," ").capitalize()}) for ip in IMPORTING_POLICY_LIST]
    return result_list

security.declarePublic('getSlotsFormingList')
def getSlotsFormingList():
    return {'default':DEFAULT_SLOT_FORMING \
           ,'data':[[s, s.replace("_"," ").capitalize()] for s in SLOT_FORMING_LIST]}

security.declarePublic('getMainColumnList')
def getMainColumnList():
    return {'default':DEFAULT_MAIN_COLUMN \
           ,'data':[[s, s.capitalize()] for s in MAIN_COLUMN_LIST]}

security.declarePublic('isValidProductName')
def isValidProductName(product_name):
    """ Check for product presence in installed products list"""
    return (product_name not in get_product_listdirs() \
            and isValidDirName(product_name))

DIR_NAME_PATTERN = re.compile("^[a-zA-Z]+[a-zA-Z0-9_]*[a-zA-Z0-9]$")
security.declarePublic('isValidDirName')
def isValidDirName(dir_name):
    """ Check for validity directory name"""
    m = DIR_NAME_PATTERN.match(dir_name)
    return m and dir_name == m.group()

security.declarePublic('createProduct')
def createProduct(context, \
                  zmi_skin_names=['custom',], \
                  zmi_base_skin_name='', \
                  subdir=None,\
                  fs_skin_directory='custom',\
                  fs_product_name='QSkinTemplate',\
                  erase_from_skin=0,\
                  doesCustomizeSlots=None,\
                  left_slots=[],\
                  right_slots=[],\
                  slot_forming=DEFAULT_SLOT_FORMING,\
                  main_column=DEFAULT_MAIN_COLUMN,\
                  doesExportObjects=None,\
                  import_policy=DEFAULT_IMPORTING_POLICY,\
                  exporting_objects=[], \
                  dump_CSS=True, \
                  dump_JS=True, \
                  dump_portlets=0, \
                  dump_policy='root', \
                  dump_portlets_selection=[], \
                  dump_custom_views=False):
    """ Main Skin Product creating procedure."""
    makeNewProduct(context, fs_product_name, fs_skin_directory, \
                   zmi_skin_names, zmi_base_skin_name, subdir, \
                   doesCustomizeSlots, left_slots, right_slots, slot_forming, main_column, \
                   doesExportObjects, import_policy, \
                   dump_CSS, dump_JS, dump_portlets, dump_policy, dump_portlets_selection, dump_custom_views)
    dumpSkin(context, zmi_skin_names, fs_product_name, erase_from_skin)
    result = exportObjects(context, doesExportObjects, exporting_objects, fs_product_name)
    return result

security.apply(globals())