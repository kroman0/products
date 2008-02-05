from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.CMFCorePermissions import ManagePortal

from Products.qPloneComments.config import *

import string
    
def install(self):
    out=StringIO()
    skinsTool = getToolByName(self, 'portal_skins')
    # Add directory views
    try:  
        addDirectoryViews(skinsTool, SKINS_DIR, GLOBALS)
        out.write( "Added directory views to portal_skins.\n" )
    except:
        out.write( '*** Unable to add directory views to portal_skins.\n')

    # Checking for presense SKIN_NAME Layer in available skins
    avail_skin_names = skinsTool.getSkinSelections()
    if SKIN_NAME in avail_skin_names :
        out.write("Skipping creation %s skin, %s already set up\n" % (SKIN_NAME) )
        return

    for skin in avail_skin_names:
        # Get skin's layers
        skin_layers = skinsTool.getSkinPath(skin)
        skin_layers_list = map( string.strip, string.split(skin_layers,',') )
        if not (SKIN_NAME in skin_layers_list) :
            # Insert new layer after 'custom'
            try: 
                skin_layers_list.insert(skin_layers_list.index('custom')+1 \
                                        , string.lower(SKIN_NAME) )
            except ValueError:
                skin_layers_list.append(string.lower(SKIN_NAME) )

            # Add new skin Layer
            new_skin_layers = string.join(skin_layers_list, ', ')
            skinsTool.addSkinSelection(skin, new_skin_layers)
            out.write("%s skin-layer was added to %s skin\n" % (SKIN_NAME, skin) )
        else:
            out.write("Skipping adding %s skin-layer, to %s skin\n" % (SKIN_NAME, skin) )

    # add Property sheet to portal_properies
    pp = getToolByName(self, 'portal_properties')
    if not PROPERTY_SHEET in pp.objectIds():
        pp.addPropertySheet(id=PROPERTY_SHEET, title= '%s Properties' % PROPERTY_SHEET)
        out.write("Adding %s property sheet to portal_properies\n" % PROPERTY_SHEET )
    props_sheet = pp[PROPERTY_SHEET]
    updateProperty(props_sheet, id="Email_of_discussion_manager", value="", property_type='string', out=out)
    updateProperty(props_sheet, id="Turning_on/off_notification", value="True", property_type='boolean', out=out)
    updateProperty(props_sheet, id="Turning_on/off_Moderation", value="True", property_type='boolean', out=out)
    updateProperty(props_sheet, id="Turning_on/off_Anonymous_Commenting", value="True", property_type='boolean', out=out)
    out.write("Updating properties of %s property sheet\n" % PROPERTY_SHEET )

    # Add Configlet. Delete old version before adding, if exist one.
    controlpanel_tool = getToolByName(self, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet(CONFIGLET_ID)
    controlpanel_tool.registerConfiglet(id=CONFIGLET_ID, name=CONFIGLET_NAME, category='Products',
                                        action='string:${portal_url}/qPloneComments_config',
                                        appId=PROJECTNAME, permission=ManagePortal, imageUrl='group.gif')


    
    out.write('Installation successfully completed.\n')
    return out.getvalue()


def updateProperty(pp_ps, id, value, property_type, out):
    if not pp_ps.hasProperty(id):
        pp_ps.manage_addProperty(id, value, property_type)
        out.write("Adding %s property to %s property sheet\n" % (id, PROPERTY_SHEET) )


def uninstall(self) :
    skinstool = getToolByName(self, 'portal_skins')

    for skinName in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skinName)
        path = [i.strip() for i in  path.split(',')]
        if SKIN_NAME in path:
            path.remove(SKIN_NAME)
            path = ','.join(path)
            skinstool.addSkinSelection(skinName, path)
