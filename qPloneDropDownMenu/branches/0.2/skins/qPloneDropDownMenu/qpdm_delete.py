## Script (Python) "qpdm_delete"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= submenu_path
##title=
##

from Products.CMFCore.utils import getToolByName

menu_tool = getToolByName(context, 'portal_dropdownmenu')
menuitem = menu_tool.manage_removeMenuItem(submenu_path)

path = '/'.join(submenu_path.strip().split('/')[:-1])

return context.getSubmenu(submenu=menu_tool.getSubMenuByPath(path),submenu_path=path)