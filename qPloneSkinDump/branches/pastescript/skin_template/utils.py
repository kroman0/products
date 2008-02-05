import transaction
import os, sys, re, string
from StringIO import StringIO
from time import gmtime, strftime
from zLOG import LOG, INFO
from zExceptions import BadRequest
from App.config import getConfiguration
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.%(SKIN_PRODUCT_NAME)s.config import *

######################################################################
##                      IMPORTING UTILS                             ##
######################################################################
osp = os.path
ALLOWED_IMPORT_POLICY = ["only_new", "backup", "overwrite"]
INTRO_TO_INSTANCE = "< Started copying object files from Product import directory to Instance one."
SUMMARY_TO_INSTANCE = "> Finished copying."
INTRO_TO_ROOT = "< Started import %%s file[s] with '%%s' policy."
SUMMARY_TO_ROOT = "> Finished importing."
INTRO_CLEAN = "< Started cleaning Instance import directory."
SUMMARY_CLEAN = "> Finished cleaning."
CREXP_INVALID_ID = re.compile('^The id \"(.*?)\" is invalid - it is already in use.$', re.DOTALL|re.IGNORECASE|re.MULTILINE)
CSS_BASE_IDS_QPSD053 = ['id','expression','enabled','cookable','media','rel','title','rendering']   # supporting qPSD-0.5.3 version
################    CHECK IMPORTING    ################
def checkIfImport():
    """ Return if perform importing, based on checking 
        *zexp files in <SkinProduct>/import directory.
    """
    instance_ipath, product_ipath = getImportedPathes()
    product_ilist = [i for i in os.listdir(product_ipath) \
                     if osp.isfile(osp.join(product_ipath,i)) and i.endswith('.zexp')]
    if product_ilist:
        return 1
    return 0

################    IMPORTING TO PLONE'S IMPORT DIR   ################
def getImportedPathes():
    """ Return Plone instance and Skin product import pathes."""
    # Based on instance path, construct import pathes 
    cfg = getConfiguration()
    instance_ipath = osp.join(cfg.instancehome, "import")
    product_ipath = osp.join(PRODUCTS_PATH, PRODUCT_NAME, "import")
    # Check presence of Product import directory
    if not osp.isdir(product_ipath):        
        raise BadRequest, "Skin Product's import directory '%%s' - does not exist or is'nt direcory" %% product_ipath
    # Check presence of Instance import directory
    if not osp.isdir(instance_ipath):
        raise BadRequest, "Instance import directory '%%s' - does not exist or isn't direcory" %% instance_ipath
    return [instance_ipath, product_ipath]

def copyFile(src_dir, dst_dir, f_name):
    """ Copy file from src_dir to dst_dir under original name."""
    try:
        src_file = open(osp.join(src_dir, f_name),"rb")
        dst_file = open(osp.join(dst_dir, f_name),"wb")
        dst_file.write(src_file.read())
        dst_file.close()
        src_file.close()
    except Exception, e:
        msg = "!!! In copying files from <%%s> dir to <%%s> dir exception occur. Details: %%s." %% (src_dir,dst_dir, str(e))
        print >> import_out, msg
        LOG('performImportToPortal',INFO,'copyFile', msg)

def moveToTemp(same_instance_files, instance_ipath, temp_dir_path):
    """ Move samenamed files from Instanse's dir to temp dir."""
    os.mkdir(temp_dir_path) # Create temp back_[date] dir
    try:
        [copyFile(instance_ipath, temp_dir_path, f_name) for f_name in same_instance_files]
        [os.remove(osp.join(instance_ipath, f_name)) for f_name in same_instance_files]
    except Exception, e:
        msg = "!!! Exception occur during moving files from Instance's dir to temp dir. Detaile:%%s." %% str(e)
        print >> import_out, msg
        LOG('performImportToPortal',INFO,'moveToTemp', msg)
    
def copyToInstanceImport():
    """ Perform copying imported files from <SkinProduct>/import dir
        to Plone's instance import dir.
    """
    print >> import_out, INTRO_TO_INSTANCE
    instance_ipath, product_ipath = getImportedPathes()
    # Compose temp dir back_[date] dir path in Instance import directory
    temp_dir_id = "back_%%s" %% strftime("%%Y%%m%%d%%H%%M%%S", gmtime())
    temp_dir_path = osp.join(instance_ipath, temp_dir_id)
    # Get *.zexp files from Skin Product's import dir and Plone's instance import dir files
    product_ilist = [i for i in os.listdir(product_ipath) \
                     if osp.isfile(osp.join(product_ipath,i)) and i.endswith('.zexp')]
    instance_ilist = [i for i in os.listdir(instance_ipath) \
                      if osp.isfile(osp.join(instance_ipath,i)) and i.endswith('.zexp')]
    # Check for presence samenamed files in Instance and Product import directories.
    same_instance_files = [f_name for f_name in instance_ilist if f_name in product_ilist]
    if same_instance_files:
        moveToTemp(same_instance_files, instance_ipath, temp_dir_path)
    # Copy all *zexp files from Product's import dir to Instance's import dir
    [copyFile(product_ipath, instance_ipath, f_name) for f_name in product_ilist]
    print >> import_out, SUMMARY_TO_INSTANCE
    return [instance_ipath, product_ipath, temp_dir_path, product_ilist]

################    IMPORTING TO PORTAL   ################
def importObject(portal, file_name):
    """ Work around old Zope bug in importing."""
    try:
        portal.manage_importObject(file_name)
    except:
        portal._p_jar = portal.Destination()._p_jar
        portal.manage_importObject(file_name)

def makeBackUp(portal, portal_objects, temp_dir_path, obj_id):
    """ Perfom backup same named portal objects in temp folder."""
    # Get id of temp folder-object
    durty_path,temp_id = osp.split(temp_dir_path)
    if not temp_id:
        durty_path,temp_id = osp.split(durty_path)
    # Get temp folder-object
    if temp_id not in portal_objects:
        portal.invokeFactory('Folder', id=temp_id)
        print >> import_out, "! Created '%%s' backup directory with same-ids " \
                             "objects from portal root." %% temp_id
    temp_dir = getattr(portal, temp_id)
    # Move object with same id to temp folder-object
    #get_transaction().commit(1)
    transaction.savepoint()
    obj = portal.manage_cutObjects(ids=[obj_id])
    temp_dir.manage_pasteObjects(obj)
    print >> import_out, "! '%%s' Object moved from portal root to '%%s' backup directory." %% (obj_id, temp_id)

def performImport(portal, temp_dir_path, file_name):
    """ Importing an object to portal."""
    portal_objects = portal.objectIds()
    try:
        portal.manage_importObject(file_name)
    except Exception, e:
        msg = str(e)
        is_invalid_id = CREXP_INVALID_ID.match(msg)
        if is_invalid_id:
            obj_id = is_invalid_id.group(1)
            if IMPORT_POLICY == "only_new":
                msg = "! Object with '%%s' id was not importing because it's already exist " \
                      "in portal root." %% obj_id
                print >> import_out, msg
            elif IMPORT_POLICY == "backup":
                makeBackUp(portal, portal_objects, temp_dir_path, obj_id)
                importObject(portal, file_name)
            elif IMPORT_POLICY == "overwrite":
                portal.manage_delObjects(ids=[obj_id])
                importObject(portal, file_name)
        else:
            # work around old Zope bug in importing
            portal._p_jar = portal.Destination()._p_jar
            portal.manage_importObject(file_name)

def importToPortalRoot(portal, product_file_names, temp_dir_path):
    """ Import all objects from *zexp files to portal root (based on IMPORT_POLICY)."""
    if not IMPORT_POLICY in ALLOWED_IMPORT_POLICY:
        raise Exception("%%s - wrong import policy in '%%s/config.py' file. Must be one of the %%s" \
                        %% (IMPORT_POLICY, PRODUCT_NAME, ALLOWED_IMPORT_POLICY) )
    print >> import_out, INTRO_TO_ROOT %% (product_file_names, IMPORT_POLICY)
    for file_name in product_file_names:
        try:
            performImport(portal, temp_dir_path, file_name)
        except Exception, error:
            msg = '!!! Under "%%s" policy importing exception occur: %%s.' %% (IMPORT_POLICY, str(error))
            print >> import_out, msg
            LOG('performImportToPortal',INFO,'importToPortalRoot', msg)
    print >> import_out, SUMMARY_TO_ROOT

################    CLEANING PLONE'S IMPORT DIR   ################
def cleanInstanceImport(instance_ipath, product_file_names, temp_dir_path):
    """ Cleaning Plone's import dir."""
    print >> import_out, INTRO_CLEAN
    # Erase all copied *zexp files from Instance's import dir
    for f_name in product_file_names:
        f_path = osp.join(instance_ipath, f_name)
        if osp.exists(f_path) and osp.isfile(f_path):
            os.remove(f_path)
        else:
            msg = '! "%%s" file was not deleted from "%%s" import directory.' %%\
                   (f_name, osp.join(instance_ipath))
            print >> import_out, msg
            LOG('performImportToPortal',INFO,'cleanInstanceImport', msg)
    # Move all files from temp back_[date] dir to Instance's import dir
    if osp.exists(temp_dir_path) and osp.isdir(temp_dir_path):
        f_names = os.listdir(temp_dir_path)
        try:
            [copyFile(temp_dir_path, instance_ipath, f_name) for f_name in f_names]
            [os.remove(osp.join(temp_dir_path, f_name)) for f_name in f_names]
            # Erase temp back_[date] dir
            os.rmdir(temp_dir_path)
        except Exception, e:
            msg = "!!! In moving files from temp dir to Instance's import dir exception occur."
            print >> import_out, msg
            LOG('performImportToPortal',INFO,'moveFromTempToImport', msg)
    print >> import_out, SUMMARY_CLEAN

################    MAIN    ################
def performImportToPortal(portal):
    """ Import objects from Skin Product to Portal root."""
    globals()['import_out'] = StringIO()
    instance_ipath, product_ipath, temp_dir_path, product_file_names = copyToInstanceImport()
    if product_file_names:
        importToPortalRoot(portal, product_file_names, temp_dir_path)
        cleanInstanceImport(instance_ipath, product_file_names, temp_dir_path)
    else:
        print >> import_out, "!!! Failure importing: there is no file for importing to be found."
    result = import_out
    del globals()['import_out']
    return result.getvalue()

######################################################################
##              INSTALLATION/UNINSTALLATION UTILS                   ##
######################################################################
CSS_REG_PROPS = ['id', 'expression', 'enabled', 'cookable', 'cacheable' \
                ,'media', 'rel', 'title', 'rendering', 'compression']
JS_REG_PROPS = ['id', 'expression', 'enabled', 'cookable', 'cacheable' \
               ,'inline', 'compression']

def installSkin(portal, pp_up, out):
    # Checking for presense SKIN_NAME in portal_skins directory view or among Skin Names
    skinsTool = getToolByName(portal, 'portal_skins')
    # Get unique product_skin_name and remember it in case of differ from SKIN_NAME.
    product_skin_name = SKIN_NAME
    skin_names = skinsTool.getSkinSelections()
    if product_skin_name in skin_names:
        idx = 0
        while product_skin_name in skin_names:
            product_skin_name = SKIN_NAME + str(idx)
            idx += 1
        addProperty(pp_up, 'q_actual_skin_name', product_skin_name, 'string', out)
    # Add directory views
    layer_skin_name = string.lower(SKIN_NAME)
    addDirectoryViews(skinsTool, 'skins', GLOBALS)
    print >> out,  "- added '%%s' directory views to portal_skins." %% layer_skin_name
    # Get Default skin and remember it for backup on uninstallig
    default_skin = skinsTool.getDefaultSkin()
    addProperty(pp_up, 'q_default_skin', default_skin, 'string', out)
    # Building list of layers for NEW SKIN
    base_path = skinsTool.getSkinPath(BASE_SKIN_NAME)
    new_path = map( string.strip, string.split(base_path,',') )
    if layer_skin_name in new_path :
        print >> out, "- %%s layer already present in '%%s' skin." %% (layer_skin_name, BASE_SKIN_NAME)
        # Remove layer_skin_name from current position.
        del new_path[new_path.index(layer_skin_name)]
    # Add layer_skin_name just after 'custom' position
    try: 
        new_path.insert(new_path.index('custom')+1, layer_skin_name)
    except ValueError:
        new_path.append(layer_skin_name)
    new_path = string.join(new_path, ', ')
    # Add NEW Skin and set it as dafault
    skinsTool.addSkinSelection(product_skin_name, new_path, make_default=1)
    print >> out, "Added %%s skin, bassed on %%s and set as default." %% (product_skin_name, BASE_SKIN_NAME)

def uninstallSkin(skinsTool, actual_skin_name, initial_skin):
    # Get 'portal_skins' object and list available skin names
    # And remove SKIN_NAME from available skins, if it present
    skin_names = skinsTool.getSkinSelections()
    if actual_skin_name in skin_names :
        skinsTool.manage_skinLayers(chosen=(actual_skin_name,), del_skin=1, REQUEST=None)
        skin_names.remove(actual_skin_name)
    # Remove product skin directory from skins tool 
    # AND Remove skin-product layer from available skins
    skin_layer = SKIN_NAME.lower()
    if skin_layer in skinsTool.objectIds():
        skinsTool.manage_delObjects(skin_layer)
    for skin_name in skin_names:
        path = skinsTool.getSkinPath(skin_name)
        path = [i.strip() for i in  path.split(',')]
        if skin_layer in path:
            path.remove(skin_layer)
            path = ','.join(path)
            skinsTool.addSkinSelection(skin_name, path)
    # If current default skin == actual_skin_name
    # Set default skin in initial one (if initial skin still exist) 
    # or in 1st from available skin names list.
    current_default_skin = skinsTool.getDefaultSkin()
    if current_default_skin == actual_skin_name:
        if initial_skin in skin_names :
            skinsTool.manage_properties(default_skin=initial_skin, REQUEST=None)
        elif len(skin_names)>0 :
            skinsTool.manage_properties(default_skin=skin_names[0], REQUEST=None)

def addProperty(p_sheet, p_id, p_value, p_type, out):
    if p_sheet.hasProperty(p_id):
        p_sheet._delProperty(p_id)
    p_sheet._setProperty(p_id, p_value, p_type)
    print >> out, "... added %%s PropertySheet to %%s." %% (p_id, p_sheet.getId())

def getResourceProperties(obj, prop_list, dflt=''):
    """ Return list of 2 items list-[property name, property value]."""
    properties=[]
    for prop in prop_list:
        accessor = getattr(obj, 'get%%s' %% prop.capitalize(), None)
        if accessor:
            properties.append([prop, accessor() or dflt])
    return properties

def registerResource(pp_up, portal_res, resRegisterFunction, out \
                    ,RESOURCE_SKIN_LIST, SKIN_RES_REGDATA, UP_PROPERTY, RES_REG_PROPS):
    """ Register resources in portal's registry, remember existant settings."""
    # Get original registered resources
    portal_res_srings = []
    for r in portal_res.getResources():
        portal_res_srings.append(";".join(['%%s::%%s'%%(r[0],str(r[1])) \
                                for r in getResourceProperties(r, RES_REG_PROPS)]))
    addProperty(pp_up, UP_PROPERTY, portal_res_srings, 'lines', out)
    # Tune Resource registry according to new skin needs
    unexistent = [] # list of default resources, 
                    # which present in Skin-product, BUT absent in portal
    portal_res_ids = portal_res.getResourceIds()
    for res_dict in SKIN_RES_REGDATA:
        if res_dict['id'] not in portal_res_ids:
            # It's interesting - Resource Registry allow adding unexistent resource - use this
            resRegisterFunction(**res_dict)
            if res_dict['id'] not in RESOURCE_SKIN_LIST:
                unexistent.append(res_dict['id'])
        else:
            pos = portal_res.getResourcePosition(res_dict['id'])
            portal_res.unregisterResource(res_dict['id'])
            resRegisterFunction(**res_dict)
            portal_res.moveResource(res_dict['id'], pos)
    if unexistent:
        print >> out, "!!! - BAD: your Resource Regestry have'nt %%s resource(s), which may lead to some problems." %% unexistent

def getVersion(res_list):
    """Check version of skin product generator."""
    return (res_list and not '::' in res_list[0] and '0.5') or '0.7'

def uninstallResource(portal_res, original_res_list, RESOURCE_SKIN_LIST, resRegisterFunction):
    # Prepare Resource Registry data for backup to original state
    original_res_regestry = {}
    genVersion = getVersion(original_res_list)
    for rec in original_res_list:
        resource = {}
        if genVersion == '0.7':
            [resource.update({prop.split('::')[0]:prop.split('::')[1]}) for prop in rec.split(";")]
        elif genVersion == '0.5':
            props = rec.split(";")
            [resource.update({CSS_BASE_IDS_QPSD053[i]:props[i]}) for i in range(len(CSS_BASE_IDS_QPSD053))]
        original_res_regestry[resource.pop('id')] = resource
    # Work up actual Resource Registry
    res_dict = portal_res.getResourcesDict()
    for res_id in res_dict.keys():
        # Remove from Resource Registry Skin product's resources
        if res_id in RESOURCE_SKIN_LIST \
           and res_id not in original_res_regestry.keys():
            portal_res.unregisterResource(res_id)
            continue
        # Backup 'enabled' property Registry's resourses to it's original state
        if original_res_regestry.has_key(res_id):
            act_Enabled_state = res_dict[res_id].getEnabled()
            orig_Enabled_state = original_res_regestry[res_id]['enabled']
            if act_Enabled_state != orig_Enabled_state:
                pos = portal_res.getResourcePosition(res_id)
                resource = res_dict[res_id]
                res = original_res_regestry[res_id]
                portal_res.unregisterResource(res_id)
                resRegisterFunction(res_id, **res)
                portal_res.moveResource(res_id, pos)

def customizeSlots(portal, pp_up, out):
    # Get original Site's column lists
    orig_left_slots = left_column = list(portal.left_slots)
    orig_right_slots = right_column = list(portal.right_slots)
    # Save original Site's LEFT and RIGHT slots
    addProperty(pp_up, 'q_left_slots', orig_left_slots, 'lines', out)
    addProperty(pp_up, 'q_right_slots', orig_right_slots, 'lines', out)
    # blend-with-site - to portal's slots adding only new one from skin-porduct
    # blend-with-skin - portal slots forming in the following manner: 
    #                   first adding skin-porduct's slots, than new one from portal
    # replace - to portal's slots forming only from the skin-porduct's slot list
    if SLOT_FORMING == "blend_with_skin":
        left_column, right_column = formSlotsColumn(LEFT_SLOTS, RIGHT_SLOTS, 
                                                    orig_left_slots, orig_right_slots, MAIN_COLUMN)
    elif SLOT_FORMING == "blend_with_site":
        left_column, right_column = formSlotsColumn(orig_left_slots, orig_right_slots,
                                                    LEFT_SLOTS, RIGHT_SLOTS, MAIN_COLUMN )
    elif SLOT_FORMING == "replace":
        left_column, right_column = formSlotsColumn(LEFT_SLOTS, RIGHT_SLOTS, [], [], MAIN_COLUMN)
    # REPLACE SITE's column slots
    portal.left_slots = tuple(left_column)
    portal.right_slots = tuple(right_column)
    print >> out, "Complited portal slots customization ..."

# main_column ("left" / "right" / "both") mean which of the MAIN column is favour
def formSlotsColumn(main_left, main_right, slave_left=[], slave_right=[], main_column="both"):
    result_left = main_left
    result_right = main_right
    if main_column == "left":
    # 1) APPEND to MAIN_LEFT list *new for main_left column* slots from slave_left list 
    # 2) APPEND to MAIN_RIGHT list *new for both main columns* slots from slave_right
    # 3) REMOVE slots from MAIN_RIGHT list, which are *doubled* in MAIN_LEFT
        [result_left.append(slot) for slot in slave_left if slot not in result_left]
        [result_right.append(slot) for slot in slave_right \
                                   if slot not in result_right and slot not in result_left]
        [result_right.remove(slot) for slot in result_left if slot in result_right]
    elif main_column == "right":
    # 1) APPEND to MAIN_LEFT list *new for main_right column* slots from slave_left list 
    # 2) APPEND to MAIN_RIGHT list *new for both main columns* slots from slave_right
    # 3) REMOVE slots from MAIN_LEFT list, which are *doubled* in MAIN_RIGHT
        [result_right.append(slot) for slot in slave_right if slot not in result_right]
        [result_left.append(slot) for slot in slave_left \
                                  if slot not in result_left and slot not in result_right]
        [result_left.remove(slot) for slot in result_right if slot in result_left]
    elif main_column == "both":
    # 1) APPEND to MAIN_LEFT list *new for both main columns* slots from slave_left list 
    # 2) APPEND to MAIN_RIGHT list *new for both main columns* slots from slave_right
        [result_left.append(slot) for slot in slave_left \
                                  if slot not in result_left and slot not in result_right]
        [result_right.append(slot) for slot in slave_right \
                                   if slot not in result_right and slot not in result_left]
    return [result_left, result_right]

def getProperty(pp, ps, id, default=[]):
    """ Get property from portal_properties/[property_sheet]"""
    res = default
    if ps in pp.objectIds() and pp[ps].hasProperty(id):
        res = pp[ps].getProperty(id, default)
    return res


###################################
## OLD INSTALL

def prepareInstallation(portal, pp, out):
    #uninstallOtherSkinProducts(portal)
    if not ('uninstall_properties' in pp.objectIds()) :
        pp.addPropertySheet(id='uninstall_properties', title= 'uninstall_properties')
        print >> out, "Created 'portal_properties.uninstall_properties' PropertySheet (UP) for backup purpose"
    return pp.uninstall_properties
CHECKED_MESSAGE = "The base installation checkings completed."

def uninstallOtherSkinProducts(portal):
    qi=getToolByName(portal, 'portal_quickinstaller', None)
    if not qi:
        raise Exception("Can't work without QuickInstaller tool.")
    # Get installed products
    installed_products = [getattr(qi, p_dict['id']) \
                          for p_dict in qi.listInstalledProducts()
                          if p_dict['id'] != PRODUCT_NAME]
    seek_str = "%%s generated product" %% GENERATOR_PRODUCT
    installed_skin_products = []
    # Looking for installed skin-products
    for p in installed_products:
        transcript = p.getTranscriptAsText()
        if transcript.find(seek_str) >= 0 :
            installed_skin_products.append(p.getId())
    # Uninstall found skin-products
    if installed_skin_products:
        qi.uninstallProducts(products=installed_skin_products)

###################################
## Prepare UNINSTALL

def prepareUninstallSkin(portal, pp_up, out): # ??
    # Checking for presense SKIN_NAME in portal_skins directory view or among Skin Names
    skinsTool = getToolByName(portal, 'portal_skins')
    # Get unique product_skin_name and remember it in case of differ from SKIN_NAME.
    default_skin = skinsTool.getDefaultSkin()
    addProperty(pp_up, 'q_default_skin', default_skin, 'string', out)
