## Script (Python) "qpt_setproperty"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= generated_tabs=False
##title=
##

from Products.CMFCore.utils import getToolByName
changeProperties = getToolByName(context, 'portal_properties').site_properties.manage_changeProperties
if generated_tabs == 'true':
  changeProperties(disable_folder_sections=False)
else:
  changeProperties(disable_folder_sections=True)
return True

