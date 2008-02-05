## Script (Python) "qploneskindump_generate_script"
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
from Products.qPloneSkinDump.generatingTemplate import generate

REQUEST = context.REQUEST

layer_name = REQUEST.get('Layer')
skin_name = REQUEST.get('Skin')
subfolder_name = REQUEST.get('Subfolder')

generate(context, skin_name, layer_name, subfolder_name)

portal_status_message='"main_template.pt" successfully created in "portal_skins/%s/%s" folder' % (layer_name, subfolder_name)
return state.set(portal_status_message=portal_status_message)