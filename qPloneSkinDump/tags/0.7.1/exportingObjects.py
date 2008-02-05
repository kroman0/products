from App.config import getConfiguration
from Products.CMFCore.utils import getToolByName
from zExceptions import BadRequest
from zLOG import LOG, INFO
from time import gmtime, strftime
import os, os.path
osp = os.path

def copyFile(src_dir, dst_dir, f_name):
    # Copy file from src_dir to dst_dir under original name
    try:
        src_file = open(osp.join(src_dir, f_name),"rb")
        dst_file = open(osp.join(dst_dir, f_name),"wb")
        dst_file.write(src_file.read())
        dst_file.close()
        src_file.close()
    except Exception, e:
        msg = "!!! In copying files from <%s> dir to <%s> dir exception occur. Details: %s" % (src_dir,dst_dir)
        LOG('performImportToPortal',INFO,'copyFile', msg)
        
def moveToDir(file_list, src_dir_path, temp_dir_path):
    # Move files from Instanse's dir to created temp dir
    if not osp.exists(temp_dir_path):
        os.mkdir(temp_dir_path)
    try:
        [copyFile(src_dir_path, temp_dir_path, f_name) for f_name in file_list]
        [os.remove(osp.join(src_dir_path, f_name)) for f_name in file_list]
    except Exception, e:
        msg = "!!! Exception occur during moving files from Instance's dir to temp dir. Detaile:%s" % str(e)
        LOG('performImportToPortal',777,'moveToDir', msg)

###############################################################
##                         EXPORTING                         ##
###############################################################
def exportObjects(context, doesExportObjects, exporting_objects, product_name):
    # Check whether should perform exporting
    if not doesExportObjects:
        return None
    # Get Instance's exported and Product's imoprt pathes
    instance_epath, product_epath = getImportedPathes(product_name)
    # Move same named files from Instance export dir to Temp dir
    temp_dir_path, product_elist = moveSameFilesToTemp(instance_epath, product_epath, exporting_objects)
    # Export objects
    fail_export = []
    portal = getToolByName(context, 'portal_url').getPortalObject()
    for odject_id in exporting_objects:
        try:
            portal.manage_exportObject(id=odject_id)
        except:
            fail_export.append(odject_id)
    # Move exported portal *zexp objects to SkinProduct's import dir
    for f_name in os.listdir(instance_epath):
        f_path = osp.join(instance_epath, f_name)
        if f_name.endswith('.zexp') and osp.isfile(f_path) and f_name in product_elist:
            copyFile(instance_epath, product_epath, f_name)
            os.remove(f_path)
    # Clean: Move same files from temd dir to var dir
    if osp.exists(temp_dir_path) and osp.isdir(temp_dir_path):
        f_names = os.listdir(temp_dir_path)
        moveToDir(f_names, temp_dir_path, instance_epath)
        os.rmdir(temp_dir_path)
    return fail_export

def getImportedPathes(product_name):
    # Based on instance path, construct import pathes 
    cfg = getConfiguration()
    instance_epath = cfg.clienthome
    product_epath = osp.join(cfg.instancehome, 'Products', product_name, "import")
    # Check presence of Product import directory
    if not osp.isdir(product_epath):        
        raise BadRequest, "Skin Product's import directory '%s' - does not exist or isn't direcory" % product_epath
    # Check presence of Instance import directory
    if not osp.isdir(instance_epath):
        raise BadRequest, "Instance import directory '%s' - does not exist or isn't direcory" % instance_epath
    return [instance_epath, product_epath]

def moveSameFilesToTemp(instance_epath, product_epath, exporting_objects):
    # Get list of Instance's export directory and exported objects
    instance_elist = [i for i in os.listdir(instance_epath) \
                      if osp.isfile(osp.join(instance_epath,i)) and i.endswith('.zexp')]
    product_elist = ["%s.zexp" % i for i in exporting_objects]
    # Compose temp dir back_[date] dir path in Instance import directory
    temp_dir_id = "back_%s" % strftime("%Y%m%d%H%M%S", gmtime())
    temp_dir_path = osp.join(instance_epath, temp_dir_id)
    # Check for presence samenamed files in Instance export dir and among exporting_objects.
    # If so - move samenamed files from Instance export dir to temp back_[date] dir.
    same_instance_files = [f_name for f_name in instance_elist if f_name in product_elist]
    if same_instance_files:
        moveToDir(same_instance_files, instance_epath, temp_dir_path)
    return [temp_dir_path, product_elist]
