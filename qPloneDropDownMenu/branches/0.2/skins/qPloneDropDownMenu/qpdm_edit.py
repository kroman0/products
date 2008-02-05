## Script (Python) "qpdm_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= submenu_path, idx
##title=
##

req = context.REQUEST
params = {}
fields = ['title', 'url']

for item in fields:
    params[item] = str(req.get('i'+idx+'_'+item, None))

from Products.CMFCore.utils import getToolByName

menu_tool = getToolByName(context, 'portal_dropdownmenu')
menuitem = menu_tool.getMenuItemByPath(submenu_path)

menuitem.setTitle(params['title'])
menuitem.setUrl(params['url'])

return params