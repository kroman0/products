## Script (Python) "qpdm_reorder"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= submenu_path, idxs
##title=
##

from Products.CMFCore.utils import getToolByName

menu_tool = getToolByName(context, 'portal_dropdownmenu')
menuitem = menu_tool.manage_reorderItems(idxs, submenu_path)

return context.getSubmenu(submenu=menu_tool.getSubMenuByPath(submenu_path),submenu_path=submenu_path)
