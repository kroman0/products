import os, re, string, sets
from App.config import getConfiguration
from Products.CMFCore.utils import getToolByName

from config import *
from write_utils import writeProps, writeFileContent, writeObjectsMeta

CSS_PATTERN = re.compile("^.+\.css$")
JS_PATTERN = re.compile("^.+\.js$")
_write_custom_meta_type_list = [
    'Controller Page Template',
    'Controller Python Script',
    'Controller Validator',
    'DTML Method',
    'File',
    'Image',
    'Page Template',
    'Script (Python)' ]
_acceptable_meta_types = _write_custom_meta_type_list + ['Folder',]
ospJoin = os.path.join

def get_product_listdirs():
    """ Return a contents of all plugged in Products directories."""
    products = sets.Set()
    [products.update(os.listdir(product_dir)) for product_dir in Products.__path__]
    return products

def getFSSkinPath(fs_product_name, fs_skin_directory, skin_obj, subdir):
    """ Return file system skin path for subdir."""
    skinpath = "%s/%s/skins/%s" % (PRODUCTS_PATH \
                                  ,fs_product_name \
                                  ,fs_skin_directory)
    # If in skin's subfolder - get its path
    skinp, subp = [obj.getPhysicalPath() for obj in [skin_obj, subdir]]
    if len(subp) != len(skinp):
        # adapt skinpath for creating directory
        skinpath += '/' + '/'.join( subp[len(skinp):] )
    return skinpath

def get_id(obj):
    """ Get real object's id."""
    id = callable(obj.id) and obj.id() or obj.id
    assert obj.getId() == id, "expected identical ids: '%s' != '%s'" % (obj.getId(), id)
    return id

def getData(obj, meta_type):
    """ Return object's data."""
    return meta_type in ['Image', 'File'] and obj.manage_FTPget() or obj.document_src()

def dumpSkin(context, \
             skin_name='custom', \
             subdir=None, \
             fs_skin_directory='custom', \
             fs_product_name='QSkinTemplate', \
             erase_from_skin=0):
    """Dump custom information to file."""
    # In case of recursable call go into subdir in skin folder.
    skin_obj = getToolByName( context, 'portal_skins' )[skin_name]
    subdir = subdir or skin_obj
    skinpath = getFSSkinPath(fs_product_name, fs_skin_directory, skin_obj, subdir)
    # Create directory in FS if not yet exist
    if not os.path.exists( skinpath ):
        os.makedirs( skinpath )
    # Loop of copying content from ZMIskin-folder to FSskin-folder 
    deletelist = []
    obj_meta = {}
    for o in subdir.objectValues():
        meta_type = o.meta_type
        id = get_id(o)
        if meta_type in _acceptable_meta_types:
            # Adding to .objects all acceptable meta_types.
            # Fixing bug of id-meta_type confusing.
            obj_meta[id] = meta_type
        if meta_type == 'Folder':
            # very plone specific
            if id in ['stylesheet_properties', 'base_properties'] \
               or id.startswith('base_properties'):
                writeProps( o, skinpath, extension = '.props' )
            else:
                dumpSkin( context, skin_name, subdir = o,\
                          fs_skin_directory=fs_skin_directory,\
                          fs_product_name=fs_product_name,\
                          erase_from_skin = erase_from_skin )
            deletelist.append( o.getId() )
        elif meta_type in _write_custom_meta_type_list:
            #writeProps( o, skinpath )      # write object's properties
            # extract content from object(depend on metatype) and write it to the file
            writeFileContent( o, skinpath, getData(o, meta_type) )
            deletelist.append( o.getId() )
        else:
            print 'method ignoring ', meta_type
    # write '.objects' file to directory if present objects with id without extension
    if obj_meta :
        writeObjectsMeta(obj_meta, skinpath)
    # delete objects from the skin, if request
    if erase_from_skin:
        subdir.manage_delObjects( ids = deletelist )

def fillinFileTemplate(f_path_read, f_path_write=None, dict={}):
    """ Fillin file template with data from dictionary."""
    if not f_path_write:
        f_path_write = f_path_read
    f_tmpl = open(f_path_read, 'r')
    tmpl = f_tmpl.read()
    f_tmpl.close()
    f_tmpl = open(f_path_write, 'w')
    f_tmpl.write(tmpl % dict)
    f_tmpl.close()

def getResourcesList(directory, resources_list, pattern=CSS_PATTERN):
    """ Get resources list from 'directory' skin folder."""
    for o in directory.objectValues():
        meta_type = o.meta_type
        id = get_id(o)
        if meta_type == 'Folder':
            # very plone specific
            if id not in ['stylesheet_properties', 'base_properties'] \
               and not id.startswith('base_properties'):
                css_list = getResourcesList(o, resources_list, pattern)
        elif pattern.match(id):
            resources_list.append( id )
    return resources_list
 
def getResourceProperties(context, regestry_id, prop_list, dflt=''):
    """ Return list of dictionaries with all dumped resources properties."""
    properties=[]
    resource = getToolByName(context, regestry_id, None)
    if resource:
        for res in resource.getResources():
            props = {}
            for prop in prop_list:
                accessor = getattr(res, 'get%s' % prop.capitalize(), None)
                if accessor:
                    props[prop] = accessor() or dflt
            properties.append(props)
    return properties

def getResourceListRegdata(context, subdir, rsrc_pattern, rsrc_name, rsrc_reg_props):
    rsrc_list = getResourcesList(subdir, resources_list=[], pattern=rsrc_pattern)#---CSS--#000000#aabbcc
    result_rsrc_list = []
    [result_rsrc_list.append(item) for item in rsrc_list if item not in result_rsrc_list]
    skin_css_regdata = getResourceProperties(context, rsrc_name, rsrc_reg_props)   # Get Data from CSS Regestry
    return result_rsrc_list, skin_css_regdata

def copyDir(srcDirectory, dstDirectory, productName):
    """Recursive copying from ZMIskin-folder to FS one""" 
    for item in os.listdir(srcDirectory):
        src_path = ospJoin(srcDirectory, item)
        dst_path = ospJoin(dstDirectory, item)
        if os.path.isfile(src_path):
            if os.path.exists(dst_path):
                continue
            f_sorce = open(src_path,'r')
            data = f_sorce.read()
            f_sorce.close()
            f_dst = open(dst_path,'w')
            f_dst.write(data)
            f_dst.close()
        elif os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)
            copyDir(src_path, dst_path, productName)

def makeNewProduct(context, productName, productSkinName, \
                   zmi_skin_name, zmi_base_skin_name, subdir,\
                   doesCustomizeSlots, left_slots, right_slots, slot_forming, main_column, \
                   doesExportObjects, import_policy, dump_CSS, dump_JS):
    """Create new skin-product's directory and 
       copy skin-product template with little modification""" 
    products_path = PRODUCTS_PATH
    productPath = ospJoin(products_path, productName)
    if not ( productName in os.listdir(products_path) ):
        os.mkdir(productPath)
    # Form CSS and JS importing list and regestry data (looking in subdir too) for Plone 2.1.0+ 
    subdir = subdir or getToolByName( context, 'portal_skins' )[zmi_skin_name]
    result_css_list = skin_css_regdata = result_js_list = skin_js_regdata = []
    if dump_CSS:
        result_css_list, skin_css_regdata = getResourceListRegdata(context, subdir,
                                            CSS_PATTERN, 'portal_css', CSS_REG_PROPS)
    if dump_JS:
        result_js_list, skin_js_regdata = getResourceListRegdata(context, subdir,
                                            JS_PATTERN, 'portal_javascripts', JS_REG_PROPS)
    # Get Slots customization information
    if not doesCustomizeSlots:
        left_slots = right_slots = None
        slot_forming = main_column = None
    # Copy skin_template to SKIN_PRODUCT directory
    templatePath = ospJoin(products_path, PROJECTNAME, TEMPLATE_PATH)
    copyDir(templatePath, productPath, productName)
    # Form data dictionary and form Skin Product's files
    conf_dict = {"IMPORT_POLICY" : import_policy \
                ,"GENERATOR_PRODUCT" : PROJECTNAME \
                ,"SKIN_PRODUCT_NAME" : productName \
                ,"SKIN_NAME" : productSkinName \
                ,"BASE_SKIN_NAME" : zmi_base_skin_name \
                ,"DUMP_CSS": not not dump_CSS \
                ,"DUMP_JS": not not dump_JS \
                ,"CSS_LIST" : str(result_css_list) \
                ,"JS_LIST" : str(result_js_list) \
                ,"SKIN_CSS_REGDATA" : str(skin_css_regdata) \
                ,"SKIN_JS_REGDATA" : str(skin_js_regdata) \
                ,"LEFT_SLOTS" : str(left_slots) \
                ,"RIGHT_SLOTS" : str(right_slots) \
                ,"SLOT_FORMING" : slot_forming \
                ,"MAIN_COLUMN" : main_column \
                }
    sp_updated_files = ['config.py' \
                       ,'README.txt' \
                       ,ospJoin('Extensions', 'utils.py')\
                       ,ospJoin('Extensions', 'Install.py')]
    for fp in sp_updated_files:
        fillinFileTemplate(ospJoin(productPath, fp), dict=conf_dict)
